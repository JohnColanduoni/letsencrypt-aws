from subprocess import check_output, check_call, call
from shutil import rmtree, make_archive, copyfile
from os import devnull

def main():
    image_id = check_output("docker build -q .".split()).strip()
    container_id = check_output("docker create {}".format(image_id).split()).strip()
    try:
        check_call("docker cp {}:/app/.venv/lib/python2.7/site-packages lambda-build".format(container_id).split())
        try:
            check_call("docker cp {}:/app/.venv/src/acme/acme/acme lambda-build/acme".format(container_id).split())
            check_call("docker cp {}:/usr/lib/x86_64-linux-gnu/libssl.so.1.0.0 lambda-build/libssl.so.1.0.0".format(container_id).split())
            check_call("docker cp {}:/usr/lib/x86_64-linux-gnu/libcrypto.so.1.0.0 lambda-build/libcrypto.so.1.0.0".format(container_id).split())
            copyfile("letsencrypt-aws.py", "lambda-build/letsencrypt-aws.py")
            make_archive("letsencrypt-aws-lambda", "zip", "lambda-build")
        finally:
            rmtree("lambda-build", True)
    finally:
        with open(devnull, 'w') as fnull:
            call("docker rm -f {}".format(container_id).split(), stdout=fnull)

if __name__ == "__main__":
    main()
