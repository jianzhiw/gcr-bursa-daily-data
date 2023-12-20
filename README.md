https://medium.com/google-cloud/deploy-a-python-flask-server-using-google-cloud-run-d47f728cc864
docker build --tag us-west1-docker.pkg.dev/winter-anchor-259905/gcr-bursa-daily-data/gcr-bursa-daily-data . --platform linux/amd64
docker push us-west1-docker.pkg.dev/winter-anchor-259905/gcr-bursa-daily-data/gcr-bursa-daily-data   
gcloud artifacts repositories create gcr-bursa-daily-data --repository-format=docker --location=us-west1 
gcloud run deploy --image=us-west1-docker.pkg.dev/winter-anchor-259905/gcr-bursa-daily-data/gcr-bursa-daily-data --region=US-WEST1 --no-allow-unauthenticated --service-account=bigquery-stock-upload@winter-anchor-259905.iam.gserviceaccount.com --name=gcr-bursa-daily-data
