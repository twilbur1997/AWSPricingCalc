import boto3
import json


def invoke_lambda_text(payload):
    """
    Example Payload
    {
        "new_services_list": "Amazon Alpha, Amazon Beta, AWS Omega"
    }
    """
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    response = lambda_client.invoke(
        FunctionName='ReminderText',
        InvocationType='Event',
        Payload=payload
    )

def main():
    payload_dict = {}
    payload_dict["new_services_list"] = "wrist_reminder"
    payload = json.dumps(payload_dict, indent=4)

    # print(payload)
    invoke_lambda_text(payload)




if __name__ == "__main__":
    main()
