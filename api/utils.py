import re

def checkForQuery(query, items):
  lowerQuery = str.lower(query)
  queryWords = lowerQuery.split(' ')
  try:
    final = [item for item in items if all(word in str.lower(item.text) for word in queryWords)][0]
  except IndexError:
    return []
  return final


def excludeCombos(items):
    keywords = ["combo", "pc gamer", "pc armada", "notebook", "laptop"]
    return [s for s in items if not any(keyword in s.text.lower() for keyword in keywords)]


def formatPrice(num):
  if(num == 0):
    return num
  formatted = re.sub(r'[^\d.,]', '', num)
  if formatted[-3] == '.':
    formatted = formatted[:-3] + ',' + formatted[-2]

  if ',' in formatted:
    formatted = formatted.split(',')[0]
  formatted = int(formatted.replace('.', ''))
  return formatted

def formatTitle(title):
  return title.replace('\n', '')