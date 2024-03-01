# Changelog

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/).

## [2.x.x] - on future date... somewhat unreleased but promises to have a new 3.x.x be created for any breaking change

### Added
- Added IS_TERRAFORM_MODULE variable so Terraform Gitlab pipeline can run checks, but avoid deploying, Terraform modules.
- Updated Mega Linter Docker image from 7.5.0 to latest to more easily keep up to date with security updates.
- Added generic Trufflehog Gitlab job that can be used to search for secrets.
- Added needs to dependency_scanning_validation, secret_detection_validation, and
  static_application_security_testing_validation Gitlab jobs for speed.
- Various simple speed improvements to pipelines involving adding artifacts between jobs and moving jobs to different
  stages for parallelism.
- Updated several Docker images to smaller images for speed improvements.
- Added secret detection to multiple pipeline templates.
- Made all Gitlab pipelines interruptible.
- Updated PublishHelmChart.yml to support signing
- Moved Helm Gitlab job from custom devops image to alpine/helm.
- Added variable to easily be able to create signed Android apks without having to use git tags.

### Changed
- Moved spotbugs sast to semgrep because spotbugs end of life for Gitlab for Java.
- Changed variable DEPLOY_DEBUG_APK_NAME to DEPLOY_DEBUG_APK_NAMES to now support multiple Android flavors.

### Fixed
- Updated Terraform pipeline's default Docker image from light to latest tag since light is deprecated.
- Fixed trivy sbom Gitlab job not working in merge request by changing rules so kaniko publish runs with trivy sbom and
  container scan jobs run, adding checks to not overwrite docker image in repo, adding publish of latest on main branch
  for docker.
- Added Helm OCI compatibility for Harbor 2.7 and later.
- Fixed gradle sast job which was calling the wrong python script.
- Updated sast python script to list all sast vulnerabilities found instead of failing on the first vulnerability found.
- Updated Mega Linter Docker image from nvuillam to oxsecurity Docker repo.
- Fixed bug in Android Ext pipeline where couldn't add gradle extra flags.
- Fixed bug by removing and creating public directory for Gitlab pages for NPM Gitlab pipelines.

## [1.3.0] - 2023-09-25

### Added
- Added `main` branch to dev regexes.
- Added Android lint and instrumentation test jobs.
- Added test, assemble, and deploy jobs for Android release builds.
- Unified DEV_REGEX and DEV_OR_RELEASE_REGEX for Gradle Java pipeline.
- Added spotbugs, code quality, and secrete detection to NPM pipeline.
- Added AsciiDoc Gradle job.
- Added Helm Pipeline.
- Added Checkov scanning job for IaC SAST scanning.
- Added Mega Linter scanning job for generic linting.
- Added Trivy SBOM Docker job.
- Added Docker pipeline.
- Added n-tier gradle subproject handling for quality and license pages.
- Added Fortify scanning job.

### Changed
- Updated the vanilla Android pipeline to work properly and send releases over Slack.
- Moved `SSH_PRIVATE_KEY` to `BASE64_ENCODED_SSH_PRIVATE_KEY` to handle base 64 encoded SSH keys for Ansible.

### Fixed
- Added `HTTP_CONNECTION_TIMEOUT_MS` and `HTTP_SOCKET_TIMEOUT_MS` variables to Install4J job to increase timeouts for
  large installer publishes.

## [1.2.0] - 2022-09-15

### Added
- Added NPM pipeline.
- Added WebTAK pipeline.
- Added Terraform pipeline.
- Added Ansible pipeline.
- Added Packer pipeline.
- Added license report multi-module aggregation.
- Added report generation for gl-sast-report.json.
- Added aggregation of JavaDocs for multimodule projects.
- Integrated SAST into Gradle Java pipeline.
- Added a license scanning job.
- Updated quality reporting to support multimodule repos.
- Added Gradle Plugin release pipeline.
- Added support for multiple page generation.
- Added a quality check job.
- Added Jacoco report coverage.

## [1.1.0] - 2021-11-7

### Changed
- Updated docker `jib` job to take credentials as an argument if config file is not present

## [1.0.0] - 2021-06-20

### Added
- Initial release mirroring the capabilities pulled from existing standardized pipelines used at CTI.
- Initial migration and publication of templates to a public repo for shared usage across GitLab instances
