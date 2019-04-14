import re


class Yamato:
  SEARCH_QUERY = 'from: mail@kuronekoyamato.co.jp AND (subject: お荷物お届けのお知らせ OR subject: 再配達依頼受付完了のお知らせ)'
  PATTERNS = {
    'parcel_and_date': [
      {
        'name': '宅配便の到着予定',
        'regex': r"(.+) 様からのお荷物を　【(.+)】　にお届け予定です。",
      },
    ],
    'date_only': [
      {
        'name': '不在のお知らせ',
        'regex': r"(.+)にお届けに参りましたが、ご不在でしたので持ち帰りました。",
      },
      {
        'name': '再配達のお知らせ',
        'regex': r"■ご希望日時　　　：(.+)",
      },
    ]
  }

  def __init__(self):
    self.patterns = {}
    for key, part_of_patterns in self.PATTERNS.items():
      self.patterns[key] = list(map(lambda v: {
        'name': v['name'], 'regex': re.compile(v['regex'])
      }, part_of_patterns))

  def get_parcel_and_date(self, message=None):
    if not message:
      raise ValueError('Empty in message')

    result = {}
    for pattern in self.patterns['parcel_and_date']:
      match = pattern['regex'].search(message)
      if match:
        result['parcel'] = match.group(1)
        result['date'] = match.group(2)
        result['name'] = pattern['name']
        break
    if not result:
      for pattern in self.patterns['date_only']:
        match = pattern['regex'].search(message)
        if match:
          result['parcel'] = None
          result['date'] = match.group(1)
          result['name'] = pattern['name']
          break
    if not result:
      result['parcel'] = result['date'] = result['name'] = None
    
    return result
