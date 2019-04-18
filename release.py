import os
import zipfile
import boto3


DEST_FOLDER = os.path.dirname(os.path.abspath(__file__))

'''
aws 자격 증명은 기본 aws console에 지정 되어 있는 프로필을 따릅니다.
aws의 설정파일 credentials의 profile을 사용 하려면 boto3.session을 이용 해 주세요.

session = boto3.Session(
    profile_name='noel'
)

boto3.resource => session.resource
'''

S3_BUCKET_NAME = 'forum.adsocialite.kr.lambda'
LAMBDA_FUNCTION_NAME = 'website_status_checker'


def create_zip():
    checker_folder = os.path.join(DEST_FOLDER, 'checker')
    checker_zip = zipfile.ZipFile(os.path.join(DEST_FOLDER, 'checker.zip'), 'w')
    for folder, subfolders, files in os.walk(checker_folder):
        for file in files:
            checker_zip.write(os.path.join(folder, file),
                      os.path.relpath(os.path.join(folder, file), checker_folder),
                      compress_type=zipfile.ZIP_DEFLATED)
    checker_zip.close()


def zip_s3_upload():
    bucket_name = S3_BUCKET_NAME
    key = os.path.join(DEST_FOLDER, 'checker.zip')
    output_name = 'checker.zip'
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(key, bucket_name, output_name)


def refresh_lambda():
    create_zip()
    zip_s3_upload()
    aws_lambda = boto3.client('lambda')
    response = aws_lambda.update_function_code(
        FunctionName=LAMBDA_FUNCTION_NAME,
        S3Bucket=S3_BUCKET_NAME,
        S3Key='checker.zip',
        Publish=True
    )
    return print(response['LastModified'])


if __name__ == "__main__":
    refresh_lambda()
