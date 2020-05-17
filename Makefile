.ONESHELL:
.SHELL := /usr/bin/bash
.PHONY: helm-target chart-repo templates charts _collect_local_helm_packages _collect_stable_helm_dependencies _set-env

# NOTE: Adjust the remote path
local := http:\/\/127.0.0.1:8879\/
remote := s3:\/\/olmax-helmchart-001-repo-eu-central-1\/charts

APP_NAMESPACE = ${AWS_PROFILE}-${PROJECT_SLUG}-${PROJECT_VERSION}
CURRENT_FOLDER=$(shell pwd)
BOLD=$(shell tput bold)
RED=$(shell tput setaf 1)
GREEN=$(shell tput setaf 2)
YELLOW=$(shell tput setaf 3)
RESET=$(shell tput sgr0)

target: help
	$(info ${HELP_MESSAGE})
	@exit 0

help:
	@echo "$(YELLOW)$(BOLD)[INFO] ...::: WELCOME :::...$(RESET)"
	head -n 5 ./LICENCE && tail -n 2 ./LICENCE && printf "\n\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

chart-repo: _set-env ## Create an s3 Helm repo Bucket - see Readme.md for further instructions
	aws cloudformation --profile ${AWS_PROFILE} --region ${AWS_REGION} create-stack --stack-name ${PROJECT_NAME}-helmcharts-${PROJECT_VERSION} \
	--template-body file://cloudformation/development/cloudformation.dev.helmchart.repo.yml \
	--parameters ParameterKey="HelmchartBucket",ParameterValue="olmax-helmchart-001-repo-${AWS_REGION}"

charts: _set-env ## Update, build packages locally and sync with remote Helm repo. Ensure that local helm server is up.
	@echo "$(YELLOW)$(BOLD)[INFO] Update local build packages and Charts in .helm-repo.$(RESET)"
	mkdir -p ${CURRENT_FOLDER}/.helm-repo
	@$(MAKE) _collect_local_helm_packages
	helm repo index ./.helm-repo
	helm repo update
	@echo "$(YELLOW)$(BOLD)[INFO] Sync local .helm-repo with remote Helm repository.${APP_NAMESPACE}.$(RESET)"
	@scripts/sync-repo.sh .helm-repo olmax-helmchart-001-repo-eu-central-1/charts ${AWS_PROFILE}
	helm search olmax/ --devel

helm-target: charts ## Deploy a target Chart via Helm install
	@echo "$(YELLOW)$(BOLD)[INFO] Deploy Helm Chart into k8s namespace ${APP_NAMESPACE}.$(RESET)"; echo "After more than 300 seconds the deploy is automatically marked as FAILED."
	@read -p "Deploy target [flask-nginx-celery]: " DATA && DATA=$${DATA:-"flask-nginx-celery"}
	@read -p "Select values [values.yaml]: " FILE && FILE="$${DATA}/$${FILE:-"$${DATA}/values.yaml"}" && \
		helm install -f $$FILE --dry-run --debug --name ${PROJECT_SLUG}-$$DATA --namespace ${APP_NAMESPACE} olmax/$$DATA
	@while [ -z "$$CONTINUE" ]; do \
        read -r -p "$(BOLD)Do you want to continue the Deployment? [$${FILE}]$(RESET) [y/N]: " CONTINUE; \
    done ; \
    [ $$CONTINUE = "y" ] || [ $$CONTINUE = "Y" ] || (echo "Helm install aborted. Exit."; exit 1;) && \
	helm install -f $$FILE --timeout 300 --wait --name ${PROJECT_SLUG}-$$DATA --namespace ${APP_NAMESPACE} olmax/$$DATA && \
	helm list -c ${PROJECT_SLUG}-$$DATA

changelog: _set-env ## Create a new temp changelog - use https://www.conventionalcommits.org/en/v1.0.0/
	@echo "$(YELLOW)$(BOLD)[INFO] Create new changelog from git in .auto-changelog.md.$(RESET)"
	cd webapiservice && PYTHONPATH=${CURRENT_FOLDER} pipenv run auto-changelog \
	--repo ${CURRENT_FOLDER} --output ${CURRENT_FOLDER}/.auto-changelog.md \
	--unreleased --latest-version "${PROJECT_SLUG} ${PROJECT_VERSION}"

#############
#  Helpers  #
#############

_collect_local_helm_packages: _collect_stable_helm_dependencies
	$(info $(BOLD)[+] Collect all local helm charts and validate templates ==> Linting ..$(RESET))
	for x in */requirements.*; do echo "Change repo target for $$x" sed -i -e "s/${remote}/${local}/g" $$x; done
	for x in */Chart.yaml; \
	do
		helm lint $$(dirname $$x)
		helm package -u -d .helm-repo $$(dirname $$x) --save
		find $$(dirname $$x) -type f -name '*.tgz' -exec cp '{}' ${CURRENT_FOLDER}/.helm-repo ';'
	done
	for x in */requirements.*; do sed -i -e "s/${local}/${remote}/g" $$x; done

_collect_stable_helm_dependencies: _set-env
	$(info $(BOLD)[+] Update dependencies in local helm chart index ..$(RESET))
	cd flask-nginx-celery/ && helm dep update && cd ..

_set-env: ## Confirm that all required Environment Variables have been set.
	@if [ -z $(AWS_PROFILE) ]; then \
		echo "$(BOLD)$(RED)AWS_PROFILE was not set$(RESET)"; \
		ERROR=1; \
	 fi
	@if [ -z $(AWS_REGION) ]; then \
		echo "$(BOLD)$(RED)AWS_REGION was not set$(RESET)"; \
		ERROR=1; \
	 fi
	@if [ -z $(PROJECT_NAME) ]; then \
		echo "$(BOLD)$(RED)PROJECT_NAME was not set$(RESET)"; \
		ERROR=1; \
	 fi
	@if [ -z $(PROJECT_SLUG) ]; then \
		echo "$(BOLD)$(RED)PROJECT_SLUG was not set$(RESET)"; \
		ERROR=1; \
	 fi
	@if [ -z $(PROJECT_VERSION) ]; then \
		echo "$(BOLD)$(RED)PROJECT_VERSION was not set.$(RESET)"; \
		ERROR=1; \
	 fi
	@if [ ! -z $${ERROR} ] && [ $${ERROR} -eq 1 ]; then \
		echo "$(BOLD)Example usage: \`AWS_PROFILE=my_profile PROJECT_NAME=olmax-baseproject PROJECT_SLUG=baseapi PROJECT_VERSION="0-0-1" AWS_REGION=eu-central-1 make charts\`$(RESET)"; \
		exit 1; \
	 fi


define HELP_MESSAGE

	Environment variables to be aware of or to hardcode depending on your use case:

	AWS_REGION
		Default: not_defined
		Info: Environment variable to declare the default AWS Region (aws configure)

	AWS_PROFILE
		Default: not_defined
		Info: Environment variable to declare which configured aws-profile to use (aws configure)

	PROJECT_NAME
		Default: not_defined
		Info: Environment variable to declare company and/or project name

	PROJECT_SLUG
		Default: not_defined
		Info: Think of a very short form of the project name with only lower-case letters and no special chars

	PROJECT_VERSION
		Default: not_defined
		Info: Project version mainly for running multiple dev environments in parallel

	$(GREEN)Common usage:$(RESET)

	$(BOLD)...::: Get a subchart manually from official Helm repo - eqivalent to 'helm dep update' :::...$(RESET)
	$(GREEN)~$$$(RESET) helm fetch --untar -d flask-nginx-celery/charts/ stable/redis

	$(BOLD)...::: Update local index and sync helm packages remote and locally :::...$(RESET)
	$(GREEN)~$$$(RESET) AWS_PROFILE=my_profile make charts

	$(BOLD)...::: Run a Helm package locally, i.e. flask-nginx-celery - ensure that subcharts are being fetched :::...$(RESET)
	$(GREEN)~$$$(RESET) AWS_PROFILE=my_profile make helm-target

	$(BOLD)...::: Develop in Minikube with Skaffold :::...$(RESET)
	$(GREEN)~$$$(RESET) AWS_PROFILE=my_profile skaffold dev --default-repo <ecr S3 repo> --kube-context local-minikube

	$(BOLD)...::: Stop and remove a running Helm package :::...$(RESET)
	$(GREEN)~$$$(RESET) helm list --all
	$(GREEN)~$$$(RESET) helm delete <helm release name> --purge

	$(BOLD)...::: Create or update the auto-changelog file :::...$(RESET)
	$(GREEN)~$$$(RESET) AWS_PROFILE=my_profile make changelog

endef
