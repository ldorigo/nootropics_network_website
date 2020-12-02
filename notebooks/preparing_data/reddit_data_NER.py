# %%
#
from json.decoder import JSONDecodeError
import spacy
import json
from json import JSONDecodeError

try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config
from tqdm.auto import tqdm
from spacy.matcher import PhraseMatcher
from pathlib import Path

nlp = spacy.load("en_core_web_sm")

# Initialize a spacy matcher. We want to match on lowercase tokens.
matcher = PhraseMatcher(nlp.vocab, attr="LOWER", validate=True)
# %%
# Load the list of synonyms  and titles from file
with open(Config.Path.synonym_mapping) as f:
    synonyms = json.load(f)

with open(Config.Path.substance_names) as f:
    names = json.load(f)

# %%
# Make a dictionary that maps substances to a list of spacy docs containing their synonym
words_to_patterns = {synonyms[i]: [] for i in synonyms}
words_to_patterns.update({name: [] for name in names})

for synonym in tqdm(synonyms):
    word = synonyms[synonym]
    words_to_patterns[word].append(nlp.make_doc(synonym))

for name in tqdm(names):
    words_to_patterns[name].append(nlp.make_doc(name))
# %%
# Add all patterns to the matcher

for word in tqdm(words_to_patterns):
    matcher.add(word, words_to_patterns[word])


submissions_path = Path().cwd() / "private_data" / "reddit_data" / "submissions"
comments_path = Config.Path.private_data_folder / "reddit_data" / "comments"
# %%

submission_files = list(submissions_path.glob("**/*"))
comments_files = list(comments_path.glob("**/*"))

# %%
def get_submissions_generator(submission_files):
    for file in tqdm(submission_files):
        with open(file, "r") as f:
            try:
                yield (json.load(f), file)
            except JSONDecodeError:
                pass
    for file in tqdm(comments_files):
        with open(file, "r") as f:
            try:
                yield (json.load(f), file)
            except JSONDecodeError:
                pass


# %%
def get_submission_doc_generator(submissions_generator):
    for submission, path in submissions_generator:
        try:
            text = submission["title"] + " " + submission["content"]
        except:
            text = submission["body"]
        yield (nlp.make_doc(text), submission, path)
        # yield nlp(test_text)


#%%
submission_generator = get_submissions_generator(submission_files=submission_files)
submission_doc_generator = get_submission_doc_generator(submission_generator)


# %%
match_generator = (
    (matcher(text), submission, path)
    for text, submission, path in submission_doc_generator
)
# %%

submissions_dict = {}
for matches, submission, path in match_generator:
    # Get the found mathches actual name
    matches_resolved = [matcher.vocab[match[0]].text for match in matches]
    # Eliminate duplicates
    matches_unique = list(set(matches_resolved))
    if not matches_unique:
        continue
    # Add to the submission and save back to file. Also add to large reddit dictionnary
    submission["matches"] = matches_unique
    with open(path, "w") as f:
        json.dump(submission, f)
    submissions_dict[submission["id"]] = submission
# %%
# Save full reddit data to file:

with open(Config.Path.reddit_data_with_NER, "w+") as f:
    json.dump(submissions_dict, f)
# with open(Config.Path.reddit_data_with_NER, "r+") as f:
# submissions_dict = json.load( f)

# %%
# Let's save a  mapping between substances and posts in which they appear

posts_per_substance = {substance: [] for substance in names}

for id in submissions_dict:
    for substance in submissions_dict[id]["matches"]:
        posts_per_substance[substance].append(id)
# %%
with open(Config.Path.posts_per_substance, "w+") as f:
    json.dump(posts_per_substance, f)
# %%
