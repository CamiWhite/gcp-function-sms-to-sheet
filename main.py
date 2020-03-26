import re
import datetime
from googleapiclient.discovery import build

SPREADSHEET_ID = '127b8BKo6EMyu4CqMv4WSgfxH1qBXFLYJ-3fAMwTYJos'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def save_sms(request):
  """
  Retrieves the reference and cost from the sms contained in the request to append the content
  in a google sheet
  Args:
    request (flask.Request): HTTP request object.
    request.body (dictionary): The request body
    request.body.message (string): The sms content
  Returns:
    An 'Ok' message to be encapsulated in a flask response
  """
  request_json = request.get_json()

  print(request_json)
  message = request_json.get('message') or 'Empty message'
  (reference, cost) = extract_details(message)

  append_in_sheet(reference, cost)

  return 'Ok'

def append_in_sheet(reference, cost):
  """
  Appends the reference and cost into the google sheet with the current date
  Args:
    reference (string): The name of the entity who made the charge
    cost (string): The cost of the charge
  """
  sheets = build('sheets', 'v4', cache_discovery = False).spreadsheets()
  today = build_date()
  request = sheets.values().append(
    spreadsheetId = SPREADSHEET_ID,
    range = build_range(),
    valueInputOption = 'USER_ENTERED',
    body = {
      'values': [
        [today, reference, cost]
      ]
    }
  )
  request.execute()

def extract_details(message):
  """
  Extracts the reference and cost from the message using a regex
  Args:
    message (string): The sms message
  Returns:
    A tuple containing the reference and cost in the form (reference, cost)
  """
  reference = re.search(' a (.*?) desde', message).group(1)
  string_cost = re.search(' por (.*?) a ', message).group(1)
  cost = int(''.join(re.findall(r'\d+', string_cost) or '000')[0 : -2])
  return reference, cost

def build_range():
  """
  Build the sheets range in A1 format with the prefix given by the current month
  Returns:
    The range
  """
  mydate = datetime.datetime.now()
  month = mydate.strftime('%B')
  return f'{month}!A1'

def build_date():
  """
  Formats the current date as day/month/year
  Returns:
    The current date in the described format
  """
  return datetime.date.today().strftime('%d/%m/%Y')
