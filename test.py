from rake_nltk import Rake
import nltk
rake_nltk_var = Rake()
text = """World chess champion, Garry Kasparov, sees the endgame for Putin. Putin is absolute evil, he has gone insane after 22 years in power; but in his bones, he must understand he cannot go on ruling Russia when the war ends and thousands of angry soldiers return home feeling robbed"""
rake_nltk_var.extract_keywords_from_text(text)
keyword_extracted = rake_nltk_var.get_ranked_phrases()
print(keyword_extracted)