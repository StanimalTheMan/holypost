# Instapost-PG-Only (WIP)

This app will compose of an API in Django using Django Rest Framework (DRF) in order to make it easier to handle RESTFUL endpoints.
The main purpose of this app is to at its core, enforce image content moderation using AWS Rekognition and preventing negative text using AWS Comprehend. AWS Lambda will be used for scalability and to decouple the tasks of image and text processing from the main app. Users will eventually be able to follow and like among other actions, but the MVP will let users post pictures and text that pass criteria.
