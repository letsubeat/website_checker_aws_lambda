import os
import zipfile
import boto3


DEST_FOLDER = os.path.abspath('')


def create_zip():
    checker_folder = os.path.abspath('checker')
    checker_zip = zipfile.ZipFile(os.path.join(DEST_FOLDER, 'checker.zip'), 'w')
    for folder, subfolders, files in os.walk(checker_folder):
        for file in files:
            checker_zip.write(os.path.join(folder, file),
                      os.path.relpath(os.path.join(folder, file), checker_folder),
                      compress_type=zipfile.ZIP_DEFLATED)
    checker_zip.close()


def zip_s3_upload():
    bucket_name = 'forum.adsocialite.kr.lambda'
    key = os.path.join(DEST_FOLDER, 'checker.zip')
    output_name = 'checker.zip'
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(key, bucket_name, output_name)


def refresh_lambda():
    create_zip()
    zip_s3_upload()
    aws_lambda = boto3.client('lambda')
    response = aws_lambda.update_function_code(
        FunctionName='website_status_checker',
        S3Bucket='forum.adsocialite.kr.lambda',
        S3Key='checker.zip',
        Publish=True
    )
    return print(response['LastModified'])


if __name__ == "__main__":
    refresh_lambda()
