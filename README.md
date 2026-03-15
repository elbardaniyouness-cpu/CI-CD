# CI/CD Final Project (Python)

This project demonstrates a complete Continuous Integration and Continuous Delivery (CI/CD) pipeline for a Python application.

## Project Overview

The pipeline was built using the following tools:

- **GitHub Actions** for Continuous Integration
- **Tekton** for task creation and execution
- **OpenShift Pipelines** for orchestrating the CI/CD workflow
- **OpenShift Cluster** for application deployment

## CI Pipeline

The Continuous Integration pipeline includes:

1. **Linting** the Python source code
2. **Running unit tests** to validate the application

These steps are automated using **GitHub Actions**.

## Tekton Tasks

The following Tekton tasks were created:

- **Lint Task** – checks code quality
- **Unit Test Task** – runs the Python test suite
- **Build Image Task** – builds the container image
- **Deploy Task** – deploys the application to OpenShift

## OpenShift Pipeline

An OpenShift pipeline was created to execute the tasks in the following order:

1. Lint
2. Unit Test
3. Build Image
4. Deploy Application

## Deployment

The final step of the pipeline deploys the Python application to the OpenShift cluster.

## Technologies Used

- Python
- GitHub Actions
- Tekton
- OpenShift Pipelines
- OpenShift Cluster
- Container Image Build

## Purpose

The purpose of this project is to apply CI/CD concepts by automating code validation, testing, building, and deployment in a cloud-native environment.
