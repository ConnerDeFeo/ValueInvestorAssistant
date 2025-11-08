import boto3

dynamodb = boto3.resource('dynamodb')

def get_item(table_name: str, key: dict):
    table = dynamodb.Table(table_name) # type: ignore
    response = table.get_item(Key=key)
    return response.get('Item')

def put_item(table_name: str, item: dict):
    table = dynamodb.Table(table_name) # type: ignore
    table.put_item(Item=item)

def update_item(table_name: str, key: dict, update_expression: str, expression_attribute_names: dict, expression_attribute_values: dict):
    table = dynamodb.Table(table_name) # type: ignore
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )

def delete_item(table_name: str, key: dict):
    table = dynamodb.Table(table_name) # type: ignore
    table.delete_item(Key=key)