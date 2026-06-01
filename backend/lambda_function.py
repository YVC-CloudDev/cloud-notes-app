import json
import boto3
import uuid

# התחברות ל-DynamoDB והגדרת הטבלה שהקמנו
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-notes-table')

def lambda_handler(event, context):
    # הגדרת Headers עבור CORS - חובה כדי לאפשר לאתר ב-S3 לדבר עם ה-API
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # טיפול בבקשות OPTIONS (Preflight) של הדפדפן
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
        
    http_method = event.get('httpMethod', '')
    
    try:
        # 1. שליפת כל הפתקים מהטבלה (GET)
        if http_method == 'GET':
            response = table.scan()
            notes = response.get('Items', [])
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(notes)
            }
            
        # 2. הוספת פתק חדש (POST)
        elif http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            title = body.get('title')
            
            if not title:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Title is required'})
                }
            
            # יצירת מזהה ייחודי לפתק
            task_id = str(uuid.uuid4())
            item = {
                'taskId': task_id,
                'title': title
            }
            
            # שמירה בטבלה
            table.put_item(Item=item)
            
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps(item)
            }
            
        # במידה והגיעו מתודות לא נתמכות כרגע
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({'error': f'Method {http_method} not allowed'})
            }
            
    except Exception as e:
        print(f"Error expanded: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }
