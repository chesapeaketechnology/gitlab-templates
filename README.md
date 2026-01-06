# GitLab Pipeline Templates

GitLab Pipeline Templates is a collection of shared GitLab jobs and pipelines aimed at simplifying the process of
setting up and maintaining the continuous integration tasks. These templates include tasks to run build scripts, unit
tests, and to publish artifacts.

## Usage

### Versioning

It's important to understand that these templates use [Semantic Versioning](https://semver.org/) by branches in GitLab
to improve stability between changes. The format of these branch names is `release/major-version` (
e.g., `release/5`). If a major (incompatible API change) occurs then a new `release/major-version
branch will be created.

### Getting Started

Inside the root directory of your project, create a file named `.gitlab-ci.yml` and copy the content from the section(s)
below that most closely match your needs. Multiple include statements can be combined to capture all the jobs that you
want to capture in your pipeline.

### Gradle Java Pipeline

The standard gradle pipeline is the simplest way to get up and running quickly. It provides a full pipeline
configuration that will build, test, and publish jars from a project utilizing
the [Build Support Plugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.build-support) (BSP). By default,
snapshots are published whenever a branch is merged into the "default" branch. Release jars are only created when a
GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below) from a
branch match the below DEV_OR_RELEASE_REGEX variable.

#### Linked Jobs

- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)
- [Test](#gradle-test-job)
- [Publish Jar](#publish-jar-job)
- [Fortify Security Scanning](#fortify-security-scanning-job)
- [Publish Pages](#publish-pages-job)
- [Quality Reporting](#quality-reporting-job)
- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Secrets Detection](#secrets-detection-job)
- [Dependency Scanning](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Dependency-Scanning.gitlab-ci.yml)
- [Dependency Scanning](#dependency-scanning-jobs)
- [License Scanning](#license-scanning-job)
- [SAST](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST.gitlab-ci.yml)
- [SAST](#sast-jobs)
- [AsciiDoc](#asciidoc-job)
- [Gitlab Release](#gitlab-release-job)

#### Customization

| Variable                                           | Pre-Loaded** | Default Value                                                        	              | Description                                                                                                                                            	                                                     |
|----------------------------------------------------|--------------|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEFAULT_IMAGE           	                          | &check;      | openjdk:11                                                                          | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	                                                     |
| IMAGE_PREFIX                 	                     |              | 	                                                                                   | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                                                                           |
| BASE_GRADLE_FLAGS   	                              | &check;      | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest)	 | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true")                                                                                  |
| DEV_REGEX                                          | &check;      | `^develop$`\|`^v3-develop$`\|`^v2-develop$`                                         | Branch(es) jobs will be run from when new commits are made. For example, if it's desired to run jobs from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\|$^v2-develop$'` |
| RELEASE_REGEX                                      | &check;      | `^[0-9]+\.[0-9]+$\|^release\/.+$`                                                   | Release oriented jobs will be run based on this regex.                                                                                                                                                       |
| DEV_OR_RELEASE_REGEX                               | &check;      | `$DEV_REGEX\|$RELEASE_REGEX`                                                        | Dev and release oriented jobs will be run based on this regex.                                                                                                                                               |
| SAFE_TEST                                          | &check;      | false                                                                               | Boolean on whether to run the build pipeline as a test before actually deploying, when set to \"true\" the build will not publish or deploy and artifacts.                                                   |
| TASK_ARGUMENTS                                     |              |                                                                                     | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.                                                     |
| RELEASE                 	                          | &check;      | 	                                                                                   | The name that will be appended to release build artifacts. By default an release candidate will be created from this unless the value "final" is used. 	                                                     |
| GRADLE_TEST_FLAGS                 	                | &check;      | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	              | Gradle flags that will be appended when running the Test Gradle task(s). 	                                                                                                                                   |
| EXTRA_GRADLE_TEST_FLAGS                 	          |              | ""	                                                                                 | Flags that will be appended to the GRADLE_TEST_FLAGS. 	                                                                                                                                                      |
| QUALITY_CHECK_GRADLE_TASKS                 	       | &check;      | pmdMain violations -x build -x test	                                                | The gradle tasks used to run the Quality Check Gradle task(s). 	                                                                                                                                             |
| QUALITY_CHECK_DISABLED                 	           | &check;      | true	                                                                               | Boolean on whether to run the Quality Check Gitlab job(s).  	                                                                                                                                                |
| DEPENDENCY_LICENSE_SCANNING_DISABLED               | &check;      | true	                                                                               | Boolean on whether to run the Dependency License Scan Gitlab job(s).  	                                                                                                                                      |
| SAST_DISABLED                 	                    | &check;      | true	                                                                               | Boolean on whether to run the SAST Gitlab job(s).  	                                                                                                                                                         |
| FORTIFY_SCANNING_DISABLED                 	        | &check;      | true	                                                                               | Boolean on whether to run the Fortify Gitlab job(s).  	                                                                                                                                                      |
| ASCIIDOC_DISABLED                 	                | &check;      | true	                                                                               | Boolean on whether to run the AsciiDoc Gitlab job(s).  	                                                                                                                                                     |
| ASCIIDOC_GRADLE_TASKS                 	            | &check;      | createDocsDistributionZip	                                                          | The gradle tasks used to run the AsciiDoc Gradle task(s).  	                                                                                                                                                 |
| VISUALIZE_TEST_COVERAGE_DISABLED                 	 | &check;      | true	                                                                               | Boolean on whether to visualize the jacoco code coverage report. 	 	                                                                                                                                         |


** Denotes Gitlab Pipeline runner will have these variables present when manually building.

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/GradleJavaPipeline.yml
```

---

### Gradle Android Pipeline

The Gradle Android pipeline provides basic jobs for building Android APKs. When APKs are built with the Gitlab pipeline
they are posted to a Slack channel.

#### Linked Jobs

- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)
- [Android Instrumentation Tests](#android-instrumentation-tests-job)
- [SAST](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST.gitlab-ci.yml)
- [Gitlab Release](#gitlab-release-job)

#### Customization

| Variable                           | Pre-Loaded** | Default Value                                                        	                                                                                          | Description                                                                                                                                            	 |
|------------------------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEFAULT_IMAGE           	          | &check;      | theimpulson/gitlab-ci-android                                                                                                                                   | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	 |
| IMAGE_PREFIX                 	     |              | 	                                                                                                                                                               | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                       |
| APK_SLACK_CHANNEL_ACCESS_TOKEN     | &check;      |                                                                                                                                                                 | The Slack channel access token.                                                                                                                          |
| APK_SLACK_CHANNEL_ID               | &check;      |                                                                                                                                                                 | The Slack channel access ID.                                                                                                                             |
| ARTIFACT_RELEASE_URL               | &check;      |                                                                                                                                                                 | The Artifact URL to publish release apk/aars.                                                                                                            |
| ARTIFACT_SNAPSHOT_URL              | &check;      |                                                                                                                                                                 | The Artifact URL to publish snapshot apk/aars.                                                                                                           |
| ARTIFACT_REPO_PASSWORD             | &check;      |                                                                                                                                                                 | The password to publish snapshot apk/aars.                                                                                                               |
| ARTIFACT_REPO_USERNAME             | &check;      |                                                                                                                                                                 | The username to publish snapshot apk/aars.                                                                                                               |
| DEPLOY_DEBUG_APK_SLACK_MESSAGE   	 | &check;      | "Hello Team! Here is the latest debug APK from branch ${CI_COMMIT_REF_NAME}. It was triggered by: ${CI_PIPELINE_SOURCE}."	                                      | The Slack message to post in the APK channel for debug builds.                                                                                           |
| DEPLOY_DEBUG_AAR_PATH              | &check;      | `app/build/outputs/aar`                                                                                                                                         | The directory path to the debug AAR that can be space deliminated.                                                                                       |
| DEPLOY_DEBUG_APK_PATH              | &check;      | `app/build/outputs/apk`                                                                                                                                         | The directory path to the debug APK that can be space deliminated.                                                                                       |
| DEPLOY_DEBUG_APK_NAMES             | &check;      | "yourdebugapkname yourotherflavordebugapkname"                                                                                                                  | The names of the debug APKs.                                                                                                                             |
| DEPLOY_RELEASE_APK_SLACK_MESSAGE   | &check;      | "Hello Team! Here is the latest release APK triggered by tag: ${CI_COMMIT_TAG}"                                                                                 | The Slack message to post in the APK channel for release builds.                                                                                         |
| DEPLOY_RELEASE_AAR_PATH            | &check;      | `app/build/outputs/aar`                                                                                                                                         | The directory path to the release AAR.                                                                                                                   |
| DEPLOY_RELEASE_APK_PATH            | &check;      | `app/build/outputs/apk`                                                                                                                                         | The directory path to the release APK.                                                                                                                   |
| DEPLOY_RELEASE_APK_NAMES           | &check;      | "yourreleaseapkname yourotherflavorreleaseapkname"                                                                                                              | The names of the release APKs that can be space deliminated.                                                                                             |
| KEYSTORE_FILE                      | &check;      |                                                                                                                                                                 | The base64-encoded keystore file. To generate this file, after creating the .jks file from Android Studio, run the command `cat keystore.jks             | base64 > keystorefile`. Copy the contents into this variable. |
| KEYSTORE_PASSWORD                  | &check;      |                                                                                                                                                                 | The password used to sign and protect the integrity of the keystore file.                                                                                |
| KEY_ALIAS                          | &check;      |                                                                                                                                                                 | An identifying name for the key.                                                                                                                         |
| KEY_PASSWORD                       | &check;      |                                                                                                                                                                 | Password for the key (this should be the same as the keystore password).                                                                                 |
| LINT_CHECK_DISABLED                | &check;      | "false"                                                                                                                                                         | True to disable lint check.                                                                                                                              |
| RELEASE                            |              |                                                                                                                                                                 | Determines what type of apk should be produced. Leave blank to produce a debug apk or anything, like 'true', to create a release apk.                    |
| BUILD_TARGET                       | &check       | Different for different jobs.  For different flavored Android builds can put multiple build targets (i.e., `BUILD_TARGET: "testFlavor1Debug testFlavor2Debug"`) | Determines what type of apk should be produced. Leave blank to produce a debug apk or anything, like 'true', to create a release apk.                    |
| COMBINE_CODE_COVERAGE_DISABLED     | &check;      | "true"                                                                                                                                                          | Boolean on whether to run the combineCoverageReports Gitlab job. 	                                                                                       |
| VISUALIZE_TEST_COVERAGE_DISABLED   | &check;      | "true"                                                                                                                                                          | Boolean on whether to visualize the jacoco code coverage report. 	                                                                                       |
| JACOCO_OUTPUT_DIR                  | &check;      | `$PROJECT_DIR/build/reports/jacoco`                                                                                                                             | Jacoco output directory for the JACOCO_HTML_LOCATION and JACOCO_XML_LOCATION. 	                                                                          |
| JACOCO_HTML_LOCATION               | &check;      | `$JACOCO_OUTPUT_DIR/index.html`                                                                                                                                 | Jacoco HTML file location used by Gitlab for things like calculating the test coverage percentage to display in merge requests. 	                        |
| JACOCO_XML_LOCATION                | &check;      | `$JACOCO_OUTPUT_DIR/jacoco-report.xml`                                                                                                                          | Jacoco XML file location used for things like displaying a test coverage report. 	                                                                       |
| PROJECT_DIR                 	      | &check;      | ./	                                                                                                                                                             | Used to specify file paths in the combineCoverageReports and visualizeCombinedTestCoverage jobs. 	                                                       |
| MAVEN_DETECTION_DISABLED   	       | &check;      | "false"                                                                                                                                                         | True to disable dependency scanning.  	                                                                                                                  |
| SAST_DISABLED   	                  | &check;      | "" (which evaluates to false so the SAST job is turned on by default)                                                                                           | True to disable SAST scanning.  	                                                                                                                        |

** Denotes Gitlab Pipeline runner will have these variables present when manually building.

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/AndroidTemplate.yml
```

---

### Gradle ATAK Build Support Plugin (BSP) Pipeline (DEPRECATED and MARKED FOR REMOVAL FOR release/6)

The Gradle ATAK [Build Support Plugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.build-support) (BSP)
pipeline provides basic jobs for building ATAK APKs with the BSP. APKs are published by default whenever a branch is
merged into the "default" branch.

#### Linked Jobs

- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)
- [SAST](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST.gitlab-ci.yml)
- [Gitlab Release](#gitlab-release-job)

#### Customization

| Variable                             | Pre-Loaded** | Default Value                                                        	 | Description                                                                                                                                            	                                                     |
|--------------------------------------|--------------|------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RELEASE                 	            |              | 	                                                                      | The name that will be appended to release build artifacts. By default an release candidate will be created from this unless the value "final" is used. 	                                                     |
| EXTRA_GRADLE_FLAGS                 	 |              | 	                                                                      | Any extra gradle flags	                                                                                                                                                                                      |
| STANDARD_GRADLE_FLAGS   	            | &check;      | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain	  | Default Gradle flags that will be appended to all Gradle commands                                                                                                                                            |
| DEV_REGEX                            | &check;      | `^develop$`\|`^v3-develop$`\|`^v2-develop$`\|`^main$`                  | Branch(es) jobs will be run from when new commits are made. For example, if it's desired to run jobs from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\|$^v2-develop$'` |
| RELEASE_REGEX                        | &check;      | `^[0-9]+\.[0-9]+$\|^release\/.+$`                                      | Release oriented jobs will be run based on this regex.                                                                                                                                                       |
| SUPPORT_REGEX                        | &check;      | `^[0-9]+\.[0-9]+$\|^support\/.+$`                                      | Support oriented jobs will be run based on this regex.                                                                                                                                                       |
| DEV_OR_RELEASE_OR_SUPPORT_REGEX      | &check;      | `$DEV_REGEX\|$RELEASE_REGEX\|$SUPPORT_REGEX`                           | Dev, release, and support oriented jobs will be run based on this regex.                                                                                                                                     |
| DEFAULT_IMAGE           	            | &check;      | theimpulson/gitlab-ci-android                                             | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	                                                     |
| IMAGE_PREFIX                 	       |              | 	                                                                      | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                                                                           |
| REPORTS_ARTIFACT                     | &check;      | ${CI_PROJECT_DIR}/app/build/reports/tests/                             | The test artifact on the build job, typically the unit test report                                                                                                                                           |
| LINT_CHECK_DISABLED                  | &check;      | "false"                                                                | True to disable lint check.                                                                                                                                                                                  |

** Denotes Gitlab Pipeline runner will have these variables present when manually building.

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/AndroidTemplateExt.yml
```

---

### Gradle Install4J Pipeline

The gradle Install4j pipeline provides basic jobs for building installers using
the [InstallerSupportPlugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.installer-support). The default
jobs provided allow projects to create both SNAPSHOT and RELEASE installers. SNAPSHOTS are published by default whenever
a branch is merged into the "default" branch. Release installers are only created when a GitLab pipeline is manually
triggered with the "RELEASE" environment variable defined (values described below) from a branch matching the
DEV_OR_RELEASE_REGEX variable.

#### Customization

| Variable 	                           | Default Value 	                                                                    | Description 	                                                                                                                                                                                                 |
|--------------------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEFAULT_INSTALL4J_IMAGE 	            | devsecops/install4j8:1.0.0-jdk11-slim-custom 	                                     | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job. 	                                                                |
| INSTALLER_ARTIFACT_PATH 	            | build/installers 	                                                                 | The path relative to the root of the project where the build artifacts can be found. 	                                                                                                                        |
| INSTALLER_NAME 	                     | "installers"	                                                                      | The name of the installer artifacts that can be downloaded after the job completes 	                                                                                                                          |
| INSTALLER_GRADLE_COMMANDS 	          | makeAllInstallers makeAllBundles 	                                                 | Gradle commands that determine which installers should be built. If building a project with multiple installers, override this variable to build a specific installer instead of all installers. 	            |
| EXTRA_GRADLE_FLAGS                 	 |                                                                                    | Any extra gradle flags                                                                                                                                                                                        |
| STANDARD_GRADLE_FLAGS   	            | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest) | Default Gradle flags that will be appended to all Gradle commands 	                                                                                                                                           |
| INSTALL4J_VERSION 	                  | unix_8_0_11 	                                                                      | The version of Install4J used to build the installers. 	                                                                                                                                                      |
| RELEASE                 	            |                                                                                    | 	Determines what type of installer should be produced. Leave blank to produce a SNAPSHOT, 'true' or 'FINAL' to create a final release, or use any other value to produce a release candidate.                 |
| DEV_OR_RELEASE_REGEX 	               | `^develop$\|^main$\|^[0-9]+\.[0-9]+$\|^release\/.+$ \|^support\/.+$                | Dev and release oriented jobs will be run based on this regex.	                                                                                                                                               |
| JDK_SELECTOR 	                       | -PJDK=11 	                                                                         | Flag that specifies which Java version the installer should target. 	                                                                                                                                         |
| HTTP_CONNECTION_TIMEOUT_MS 	         | 30000	                                                                             | HTTP connection timeout that gets applied to Gradle HTTP. Can be useful for things like large Gradle installer publishes.  	                                                                                  |
| HTTP_SOCKET_TIMEOUT_MS 	             | 60000 	                                                                            | HTTP socket timeout that gets applied to Gradle HTTP. Can be useful for things like large Gradle installer publishes.  	                                                                                      |
| I4J_LICENSE_KEY 	                    |                                                                                    | `FLOAT:1.2.3.4` if no encryption ejt.ks auth file, `FLOAT:1.2.3.4,./ejt.ks` if encryption ejt.ks auth file which requires `EJT_LICENSE_ENCRYPTION_KEY_BASE64`  	                                              |
| EJT_LICENSE_ENCRYPTION_KEY_BASE64 	  |                                                                                    | Base64 string of EJT license server ejt.ks binary file since Gitlab cannot store binary formatted files/strings as Gitlab CI variables. Can create using `base64 --input ejt.ks --output encoded_file.txt`  	 |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/GradleInstall4JPipeline.yml
```

---

### Gradle Plugin Release Pipeline

The plugin release pipeline provides support for invoking a standard set of tasks on a gradle project that builds and
publishes a plugin to the Gradle Plugin Portal. The consuming project is expected to provide typical build/test tasks.
In addition, to support the actual release process, it must define a task named `doRelease` which, when invoked along
with the project property `-Prelease`, will build and publish the plugin to the portal.

Note that this pipeline will run tests on all feature branches, but it will only perform a release when invoked from the
GitLab web UI on the default branch of the repo and only if the `RELEASE` variable is set to `true`.

#### Customization

| Variable 	            | Default Value 	                                                                      | Description 	                                                                                                                                            |
|-----------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEFAULT_IMAGE         | eclipse-temurin:11-jdk                                                               | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.             |
| STANDARD_GRADLE_FLAGS | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain $TASK_ARGUMENTS | Default Gradle flags that will be appended to all Gradle commands                                                                                        |
| TASK_ARGUMENTS        |                                                                                      | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream. |
| RELEASE               | 'false'                                                                              | Determines if a 'release' build will be performed, which also publishes the plugin to the Gradle Plugin Portal.  Use 'true' to perform a release build.  |
| GRADLE_PUBLISH_KEY    | NONE                                                                                 | The Gradle plugin portal publishing key, must be set as an environment variable                                                                          |
| GRADLE_PUBLISH_SECRET | NONE                                                                                 | The Gradle plugin portal publishing secret, must be set as an environment variable                                                                       |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/GradlePluginReleasePipeline.yml
```

---

### Packer Pipeline

The standard Packer pipeline is the simplest way to get up and running quickly. It provides a full pipeline
configuration that will format, validate, and deploy Packer VMs from a project.

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/PackerPipeline.yml
```

---

### Terraform Pipeline

The standard Terraform pipeline is the simplest way to get up and running quickly. It provides a full pipeline
configuration that will format, validate, security test, plan, apply, and destroy Terraform Infrastructure as Code (IaC)
from a project. Can be used for any cloud environment (e.g., Azure, AWS, etc).

#### Linked Jobs

- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Gitlab SAST IaC](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST.gitlab-ci.yml)
- [Checkov IaC SAST](#checkov-iac-sast-job)
- [Gitlab Release](#gitlab-release-job)

#### Customization

| Variable            | Description                                                	                                                                                                                               |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TF_ROOT             | The root directory of your terraform project                                                                                                                                               |
| PLAN_FILE_NAME      | The Terraform state file name                                                                                                                                                              |
| TF_STATE_NAME       | The Terraform State file name                                                                                                                                                              |
| TF_CACHE_KEY        | The Terraform cache key for Gitlab caching                                                                                                                                                 |
| IMAGE_PREFIX        | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                                                         |
| DEFAULT_IMAGE       | The Docker image used for most of the Terraform Gitlab pipeline's jobs                                                                                                                     |
| DOCKER_REPO_NAME    | Docker repository name (e.g., devsecops)                                                                                                                                                   |
| TF_INIT_FLAGS       | Any flags to add to the Gitlab job's `terraform init` call                                                                                                                                 |
| IS_TERRAFORM_MODULE | Set to "true" if your Gitlab repository is a Terraform module which tells the Gitlab pipeline's jobs to not deploy code but jut run some analysis jobs like formatting and security checks |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/TerraformPipeline.yml
```

---

### Docker Pipeline

The standard Docker pipeline is the simplest way to get up and running quickly. It provides a full pipeline
configuration that will lint and apply Docker continuous deployments (CD) from a project.

#### Linked Jobs

- [Mega Linter](#mega-linter-job)
- [Kaniko Docker Image Publishing](#kaniko-docker-image-publishing-job)
- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Container Scanning](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Container-Scanning.gitlab-ci.yml)
- [SAST IaC](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST-IaC.gitlab-ci.yml)
- [Trivy SBOM](#trivy-sbom-job)
- [Checkov IaC SAST](#checkov-iac-sast-job)
- [Gitlab Release](#gitlab-release-job)

#### Customization

| Variable               | Description                                                	                                                                                                                                          |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| USE_DOCKER_AUTH_CONFIG | Defaults to "true", "true" is for using a `DOCKER_AUTH_CONFIG` for Kaniko authentication, use "false" to authenticate with `DOCKER_REPO_HOSTNAME`, `DOCKER_REPO_USERNAME`, and `DOCKER_REPO_PASSWORD` |
| DOCKER_DIRECTORY       | Optional variable to set the directory where the Dockerfile is located                                                                                                                                |
| DOCKERFILE             | Optional variable to set the name of the Dockerfile (e.g., Dockerfile.mine)                                                                                                                           |
| DOCKER_REPO_USERNAME   | Username to publish the Docker image                                                                                                                                                                  |
| DOCKER_REPO_PASSWORD   | Password to publish the Docker image                                                                                                                                                                  |
| DOCKER_REPO_HOSTNAME   | Docker repository hostname (e.g., docker-custom-local.artifacts.net)                                                                                                                                  |
| DOCKER_REPO_NAME       | Docker repository name (e.g., devsecops)                                                                                                                                                              |
| APP_NAME               | Docker image app name (e.g., MyCustomKafka)                                                                                                                                                           |
| VERSION                | Docker image version (e.g., latest)                                                                                                                                                                   |
| IMAGE_PREFIX           | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                                                                    |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/DockerPipeline.yml
```

---

### Helm Pipeline

The standard Helm pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration
that will lint and apply Helm continuous deployments (CD) from a project.

#### Linked Jobs

- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Mega Linter](#mega-linter-job)
- [Publish Helm Chart Jobs](#publish-helm-chart-jobs)
- [Checkov IaC SAST](#checkov-iac-sast-job)
- [SAST](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST.gitlab-ci.yml)
- [Gitlab Release](#gitlab-release-job)

#### Customization

| Variable     | Description                                                	                            |
|--------------|-----------------------------------------------------------------------------------------|
| IMAGE_PREFIX | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job. |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/HelmPipeline.yml
```

---

### Ansible Pipeline

The standard Ansible pipeline is the simplest way to get up and running quickly. It provides a full pipeline
configuration that will lint and apply Ansible continuous deployments (CD) from a project. Can be used for any virtual
machine host (e.g., Azure VMs, AWS VMs, local VMs, etc).

#### Linked Jobs

- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [SAST IaC](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST-IaC.gitlab-ci.yml)
- [Mega Linter](#mega-linter-job)
- [Checkov IaC SAST](#checkov-iac-sast-job)
- [Playbook Deploy](#playbook-deploy-job)
- [Gitlab Release](#gitlab-release-job)

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/AnsiblePipeline.yml
```

---

### Bash Pipeline

The standard Bash pipeline is the simplest way to get up and running quickly. It provides a full pipeline
configuration that will lint and apply Bash continuous deployments (CD) from a project.

#### Linked Jobs

- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Mega Linter](#mega-linter-job)
- [Gitlab Release](#gitlab-release-job)

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/BashPipeline.yml
```

---

### Python Pipeline

The standard Python pipeline is the simplest way to get up and running quickly. It provides a full pipeline
configuration that will lint and apply Python continuous deployments (CD) from a project.

#### Linked Jobs

- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [SAST](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST.gitlab-ci.yml)
- [Gitlab Release](#gitlab-release-job)

#### Customization

| Variable                        | Description                                                	                                                                                 |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| PYTHON_PIPELINE_IMAGE_PREFIX    | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job.                                                      |
| PYTHON_PIPELINE_DEFAULT_IMAGE 	 | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job. |
| PYTHON_ROOT                     | The directory that is the root of the Python component used by a Gitlab pipeline job.                                                        |
| PYTHON_MODULE                   | The python module(s) that should be invoked by the pytest Gitlab job, relative to PYTHON_ROOT, can be multiple modules.                      |
| PYTEST_MODULE                   | The test module(s) that should be invoked by the pytest Gitlab job, relative to PYTHON_ROOT, can be multiple modules.                        |
| MICROMAMBA_VERSION              | The docker image base for micromamba that should be used by the pytest Gitlab job.                                                           |
| MICROMAMBA_ENVIRONMENT_FILE     | The environment definition file that should be used by the pytest Gitlab job.                                                                |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/BashPipeline.yml
```

---

### NPM Unit Test and Test Coverage Pipeline

The standard NPM pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration
that will install, build, test, and provide test results and coverage reports on both merge requests and gitlab pages.

#### Requirements

The pipeline expects a `package.json` script called `test:ci`. It's recommended to follow the below setup to ensure this
pipeline works as expected.

**Install dependencies**

`npm install --save-dev jest jest-junit` or `yarn add --dev jest jest-junit`

**Add script to `package.json`**

```
"scripts": {
    [...]
    "test:ci": "jest --config ./jest.config.js --collectCoverage --coverageDirectory=\"./coverage\" --ci --reporters=default --reporters=jest-junit --watchAll=false",
}
```

**Include this configuration in `jest.config.js`**

```
module.exports = {
    [...]
    collectCoverageFrom: ['src/**/*.{js,jsx,ts,tsx}'],
    coverageReporters: ['html', 'text', 'text-summary', 'cobertura'],
}
```

#### Customization

| Variable     | Description                                                	                                      |
|--------------|---------------------------------------------------------------------------------------------------|
| IMAGE_PREFIX | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job.         	 |
| NODE_IMAGE   | The base node image used to run all jobs. (e.g. node:16)          	                               |
| TEST_ARGS    | Optional additional arguments or flags to add to the `npm test:ci` script.                        |

#### Reference URL

```
include:
    - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/NpmJestCoveragePipeline.yml

```

---

### WebTAK Plugin Test Coverage Pipeline

The standard NPM pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration
that will install, build, test, and provide test results and coverage reports on both merge requests and gitlab pages.

#### Requirements

The pipeline has this repo's `NpmJestCoveragePipeline` as an included dependency. It is necessary to follow the
requirements from that pipeline in order to use this one.

#### Linked Pipelines

- [NPM Jest Coverage Pipeline](#npm-unit-test-and-test-coverage-pipeline)

#### Customization

| Variable      | Description                                                                           |
|---------------|---------------------------------------------------------------------------------------|
| TAK_EMAIL     | A valid TAK.gov email account with access to WebTAK artifacts on the TAK Artifactory. |
| TAK_API_TOKEN | An API token generated using the same email as above.                                 |

#### Reference URL

```
include:
    - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/pipeline/WebtakTestCoverage.yml

```

---

### Gradle Test (job)

Runs tests through Gradle commands and publishes the results as an artifact to GitLab. These test result artifacts can
be viewed by going to your project's CI pipelines page and then selecting the context menu on the right hand of the test
job.

#### GitLab Artifacts

- Tests results found in the build/test-results/test/ directory. This is the default location for JUnit test results.

#### Customization

| Variable          	       | Description                                            	                                                                        |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| JACOCO_OUTPUT_DIR 	 | Jacoco output directory for the JACOCO_HTML_LOCATION and JACOCO_XML_LOCATION 	                                                  |
| JACOCO_HTML_LOCATION 	 | Jacoco HTML file location used by Gitlab for things like calculating the test coverage percentage to display in merge requests	 |
| JACOCO_XML_LOCATION 	 | Jacoco XML file location used for things like displaying a test coverage report	                                                |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/Test.yml
```

---

### Publish Jar (job)

Publishes a SNAPSHOT jar whenever a feature branch is merged into the project's default branch and publishes release
jars when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described
below). After performing a release build, the project's version is automatically updated and the change is committed to
the repo. Javadocs are also published with releases.

#### Customization

| Variable                	     | Default Value                                                        	             | Description                                                                                                                                                                               	                                          |
|-------------------------------|------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| STANDARD_GRADLE_FLAGS   	     | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest) | Default Gradle flags that will be appended to all Gradle commands  	                                                                                                                                                                 |
| PUBLISH_SNAPSHOT_GRADLE_FLAGS | 	                                                                                  | Gradle flags for customizing the snapshot publish tasks                                                                                                                                                                              |
| RELEASE_GRADLE_FLAGS          | ""                                              | Flags passed to the gradle command used to publish release jars.                                                                                                                                                                     |
| GIT_TASKS_ENABLED             | true                                                                               | Determines whether any gradle tasks that perform Git operations with be included in the pipeline. If disabled a project's version will not be automatically updated following a release build                                        |
| DEV_OR_RELEASE_REGEX          | '^develop$\|^v3-develop$\|^v2-develop$\|^main$\|^[0-9]+\.[0-9]+$\|^release\/.+$'   | Branch(es) SNAPSHOT builds will be published from when new commits are made. For example, if it's desired to build SNAPSHOTs from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\|$^v2-develop$'` |
| SAFE_TEST                     | false                                                                              | Boolean on whether to run the build pipeline as a test before actually deploying, when set to \"true\" the build will not publish or deploy and artifacts.                                                                           |
| TASK_ARGUMENTS                |                                                                                    | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.                                                                             |
| RELEASE                 	     | 	                                                                                  | The name that will be appended to release build artifacts. By default a release candidate will be created from this unless the value "final" is used   	                                                                             |
| PUBLISH_SNAPSHOT_JAR_DISABLED | 	                                                                                  | True to disable snapshot jar publishing.                                                                                                                                                                                             |
| PUBLISH_RELEASE_JAR_DISABLED  | 	                                                                                  | True to disable release jar publishing.                                                                                                                                                                                              |
| SKIP_PUBLISH_TESTS  | 	                                                                                  | True to disable tests from running inside jar publishing.                                                                                                                                                                                              |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/PublishJar.yml
```

---

### Publish Pages (job)

Publishes Gitlab Pages such as JavaDocs, coverage, quality, licenses, and vulnerabilities.

#### Customization

| Variable                	 | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|---------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FORCE_PUBLISH_PAGES   	   |                                                                        | True to force publishing of pages.  	                                                                                                                                                       |
| PUBLISH_JAVADOCS_DISABLED | 	                                                                      | True to disable JavaDoc publishing.                                                                                                                                                         |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/PublishPages.yml
```

---

### Secrets Detection (job)

Gradle job to detect secrets and put into a report.

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/SecretDetection.yml
```

---

### Quality Reporting (job)

Gradle job to scan quality and put into a report.

#### Customization

| Variable                	  | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|----------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| QUALITY_CHECK_DISABLED   	 |                                                                        | True to disable quality reporting.  	                                                                                                                                                       |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/QualityReporting.yml
```

---

### Dependency Scanning (jobs)

Jobs to scan dependency vulnerabilities of Gradle projects and put into a report.

#### Customization

| Variable                	           | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|-------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MAVEN_DETECTION_DISABLED   	        |                                                                        | True to disable dependency scanning.  	                                                                                                                                                     |
| EXCLUDED_VULNERABILITY_PACKAGES   	 |                                                                        | A comma delimited list of packages (e.g., "dom4j/dom4j,org.apache.shiro/shiro-web") to exclude from dependency vulnerability scanning	                                                      |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/DependencyScanning.yml
```

---

### SAST (jobs)

Static Application Security Testing (SAST) scanning and reports for a Gradle project.

#### Customization

| Variable                	             | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|---------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SAST_DISABLED   	                     |                                                                        | True to disable the jobs.  	                                                                                                                                                                |
| EXCLUDED_SAST_VULNERABILITY_FILES   	 |                                                                        | A comma delimited list of files (e.g., "SettingsWriter.java, MessageStructure.java") to exclude from SAST vulnerability scanning	                                                           |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/StaticApplicationSecurityTesting.yml
```

---

### License Scanning (job)

Jobs to scan licenses of Gradle projects and put into a report.

#### Customization

| Variable                	                | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEPENDENCY_LICENSE_SCANNING_DISABLED   	 |                                                                        | True to disable license scanning.  	                                                                                                                                                        |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/LicenseScanning.yml
```

---

### Asciidoc (job)

Creates AsciiDoc using a Gradle job using
the [AsciiDoc Generator Gradle Plugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.asciidoc-generator).

#### Customization

| Variable                	 | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|---------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ASCIIDOC_GRADLE_TASKS   	 |                                                                        | The AsciiDoc Gradle tasks.  	                                                                                                                                                               |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/Asciidoc.yml
```

---
### Java Gradle ATAK Offline (jobs)

A set of Gitlab jobs to build, test, etc for ATAK plugins. This template currently does not support building release ATAK 
plugin APKs as that requires the TAK.gov Gitlab CI runner to perform signing.

#### Customization

| Variable                	            | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|--------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ARTIFACT_REPO_USERNAME (REQUIRED)  	 | ""                                                                     | Artifact repository username.  	                                                                                                                                                            |
| ARTIFACT_REPO_PASSWORD (REQUIRED)  	 | ""                                                                     | Artifact repository password.                                                                                                                                                               |
| ATAK_DEV_REPO_URL (REQUIRED)  	      | ""                                                                     | Artifact repository URL for ATAK dev dependency.	                                                                                                                                           |
| ATAK_TOOL_REPO_URL (REQUIRED)        | ""                                                                     | Artifact repository URL for ATAK tool dependency.	                                                                                                                                          |
| IMAGE_PREFIX                         | ""                                                                     | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job.                                                                                                     |
| DEFAULT_IMAGE                        | "theimpulson/gitlab-ci-android:android-35-jdk-17"                      | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.                                                |
| STANDARD_GRADLE_FLAGS                | '-s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain' | Default Gradle flags that will be appended to all Gradle commands                                                                                                                           |
| EXTRA_GRADLE_FLAGS                   | "--init-script .gradle/init.d/ci-atak-repos.gradle"                    | Any extra gradle flags.                                                                                                                                                                     |
| ASSEMBLE_GRADLE_TASK (REQUIRED)      | ""                                                                     | Any extra gradle flags.                                                                                                                                                                     |
| TEST_GRADLE_TASK (REQUIRED)          | ""                                                                     | Any extra gradle flags.                                                                                                                                                                     |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/JavaGradleAtakOffline.yml
```

---

### Android Instrumentation Tests (job)

Runs Android Instrumentation Tests against an Android device/emulator using a Gradle job.

#### Customization

| Variable                	            | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|--------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ANDROID_SDK_ROOT   	                 | "/sdk"                                                                 | Android SDK root location.  	                                                                                                                                                               |
| ADB_EXECUTABLE   	                   | $ANDROID_SDK_ROOT/platform-tools/adb                                   | ADB executable location.  	                                                                                                                                                                 |
| BUILD_TARGETS   	                    | connectedDebugAndroidTest                                              | The Gradle command to run the Android instrumentation test, can give multiple Gradle commands for multiple Android flavors.	                                                                |
| ANDROID_EMULATOR_IP                  |                                                                        | IP address of emulator for instrumentation tests. Recommend to mask the IP as a Gitlab CI/CD variable.                                                                                      |
| ANDROID_EMULATOR_ADB_PORT            | 5555                                                                   | ADB port of emulator for instrumentation tests.                                                                                                                                             |
| APP_PACKAGE_NAMES_TO_FORCE_UNINSTALL |                                                                        | Name of your app's packages in case to force uninstall before running instrumentation tests.                                                                                                |

#### Reference URL

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/AndroidInstrumentationTests.yml
```

---

### Kaniko Docker Image Publishing (job)

Uses the gradle [Kaniko Docker image](https://github.com/GoogleContainerTools/kaniko) to build and publish docker
images.

#### Customization

| Variable                 | Description                                                                                                       	                                                    |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| USE_DOCKER_AUTH_CONFIG 	 | Flag to use DOCKER_AUTH_CONFIG or a combination of DOCKER_REPO_HOSTNAME, DOCKER_REPO_USERNAME, and DOCKER_REPO_PASSWORD                                              	 |
| DOCKER_DIRECTORY         | Root directory of a Dockerfile 	                                                                                                                                       |
| DOCKERFILE               | Name of the Dockerfile to build and publish                           	                                                                                                |
| DOCKER_AUTH_CONFIG       | A config with the repo, username, and password, see https://docs.gitlab.com/ee/ci/docker/using_kaniko.html for more details of config format                           |
| DOCKER_REPO_HOSTNAME     | Only needed if not using DOCKER_AUTH_CONFIG. URL to docker repository, i.e. `harbor.ctic-dev.com`                                                                      |
| DOCKER_REPO_USERNAME     | Only needed if not using DOCKER_AUTH_CONFIG. Username for that repository                                                                                              |
| DOCKER_REPO_PASSWORD     | Only needed if not using DOCKER_AUTH_CONFIG. Password for that repository                                                                                              |
| OVERWRITABLE_TAG_REGEX   | Regex of Docker image tags to not overwrite in a Docker repository                                                                                                     |
| DOCKER_BUILD_ARGS        | Docker build arguments spaced delimited                                                                                                                                |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/docker/Kaniko.yml
```

---
### Kaniko ARM Docker Image Publishing (job)

Uses [Kaniko](https://github.com/GoogleContainerTools/kaniko) to build and publish ARM-based Docker images.  
This job is designed to support multi-architecture builds alongside its AMD64 counterpart.

#### Customization

| Variable               | Description                                                                                                                                       |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `USE_DOCKER_AUTH_CONFIG` | Whether to use the `DOCKER_AUTH_CONFIG` variable for authentication. Defaults to `"true"`.                                                       |
| `DOCKER_DIRECTORY`       | Directory path containing the Dockerfile. Defaults to the root of the repository.                                                                |
| `DOCKERFILE`             | Name of the Dockerfile to use for building.                                                                                                      |
| `DOCKER_REPO_USERNAME`   | Docker registry username for authentication.                                                                                                     |
| `DOCKER_REPO_PASSWORD`   | Docker registry password or access token.                                                                                                        |
| `DOCKER_REPO_HOSTNAME`   | Hostname of the Docker registry (e.g., `harbor.mycompany.com`).                                                                                  |
| `DOCKER_REPO_NAME`       | Name of the repository within the registry.                                                                                                      |
| `APP_NAME`               | Name of the Docker image (e.g., `my-app`).                                                                                                       |
| `VERSION`                | Version tag for the image (e.g., `1.0.0-arm64`).                                                                                                 |
| `ARCHITECTURE`           | Architecture label (e.g., `arm64`) appended to the version. Used in tag construction. Optional if `VERSION` is already complete.                  |
| `IMAGE_TAG`              | Full image tag (e.g., `my-app:1.0.0-arm64`). Optional if `VERSION` and `ARCHITECTURE` are provided.                                                |

#### Example `.gitlab-ci.yml` job definition

```yaml
kaniko_publish_arm:
  extends: .kaniko_publish
  variables:
    VERSION: "1.0.0-arm64"
    APP_NAME: "my-app"
    DOCKER_REPO_NAME: "platform"
    ARCHITECTURE: "arm64"
  tags:
    - architecture-aarch64
```

---
### Multi-Architecture Manifest Publishing (job)

Creates and publishes a Docker multi-architecture manifest using the Docker CLI.  
This job combines separate platform-specific images (e.g., `amd64` and `arm64`) into a single unified image tag.  
This is useful when you want to support multiple platforms with one image reference (e.g., `my-app:1.0.0`).

#### Customization

| Variable               | Description                                                                                                 |
|------------------------|-------------------------------------------------------------------------------------------------------------|
| `DOCKER_REPO_HOSTNAME` | Hostname of the container registry (e.g., `harbor.mycompany.com`).                                          |
| `DOCKER_REPO_USERNAME` | Docker registry username.                                                                                    |
| `DOCKER_REPO_PASSWORD` | Docker registry password or token.                                                                          |
| `AMD_IMAGE`            | Full image tag of the `amd64` image (e.g., `my-repo/my-app:1.0.0-amd64`).                                   |
| `ARM_IMAGE`            | Full image tag of the `arm64` image (e.g., `my-repo/my-app:1.0.0-arm64`).                                   |
| `MULTIARCH_IMAGE`      | Final target tag for the multiarch image (e.g., `my-repo/my-app:1.0.0`).                                    |

#### Example `.gitlab-ci.yml` job definition

```yaml
multiarch_manifest_publish:
  stage: publish
  image: docker:28.4.0
  services:
    - docker:28.4.0-dind
  variables:
    DOCKER_TLS_CERTDIR: ""
    AMD_IMAGE: ""
    ARM_IMAGE: ""
    MULTIARCH_IMAGE: ""
    DOCKER_REPO_HOSTNAME: ""
  script:
    - |
      echo "$DOCKER_REPO_PASSWORD" | docker login "$DOCKER_REPO_HOSTNAME" -u "$DOCKER_REPO_USERNAME" --password-stdin
      set -e
      echo "🔧 Creating manifest from:"
      echo " - $AMD_IMAGE"
      echo " - $ARM_IMAGE"
      echo "=> $MULTIARCH_IMAGE"

      # Normalize all image references to lowercase
      LOWER_HOSTNAME=$(echo "$DOCKER_REPO_HOSTNAME" | tr '[:upper:]' '[:lower:]')
      LOWER_AMD_IMAGE=$(echo "$AMD_IMAGE" | tr '[:upper:]' '[:lower:]')
      LOWER_ARM_IMAGE=$(echo "$ARM_IMAGE" | tr '[:upper:]' '[:lower:]')
      LOWER_MULTIARCH_IMAGE=$(echo "$MULTIARCH_IMAGE" | tr '[:upper:]' '[:lower:]')

      # Create and push multi-arch manifest
      docker manifest create "$LOWER_HOSTNAME/$LOWER_MULTIARCH_IMAGE" \
        --amend "$LOWER_HOSTNAME/$LOWER_AMD_IMAGE" \
        --amend "$LOWER_HOSTNAME/$LOWER_ARM_IMAGE"

      docker manifest push "$LOWER_HOSTNAME/$LOWER_MULTIARCH_IMAGE"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "web"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---
### JIB Docker Image Publishing (job)

Uses the gradle [JIB Gradle plugin](https://github.com/GoogleContainerTools/jib/tree/master/jib-gradle-plugin) to build
and publish docker images. The
job will attempt to use your credentials stored in the `$HOME/.docker/config.json` file on the Gitlab instance running
the pipeline. If the `HOME` variable
is not set or the credentials are not present on your system, use the username and password variables detailed below.

> Note: Be sure NOT to save credentials directly to your code repository.
>
> Note: This job will only run when code is committed to the repository's default branch, i.e. it will not run in merge
> requests, and will
> instead run after the request is merged.

#### Customization

| Variable              	 | Default Value                                                        	 | Description                                                                                                       	      |
|-------------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| STANDARD_GRADLE_FLAGS 	 | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	 | Default Gradle flags that will be appended to all Gradle commands                                                 	      |
| JIB_FLAGS             	 | -DsendCredentialsOverHttp=true                                       	 | Gradle flags used to customize the JIB task. The default value enables publishing docker images to insecure registries 	 |
| DOCKER_REPO_HOSTNAME    |                                                                        | URL to docker repository, i.e. `harbor.ctic-dev.com`                                                                     |
| DOCKER_REPO_USERNAME    |                                                                        | Username for that repository                                                                                             |
| DOCKER_REPO_PASSWORD    |                                                                        | Password for that repository                                                                                             |
| PUBLISH_DOCKER        	 |                                                                        | Flag to manually publish a docker image from a GitLab pipeline on a non-default branch                           	       |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/docker/Jib.yml
```

---

### IMG Docker Image Publishing (job)

Uses the [IMG toolchain](https://github.com/genuinetools/img) to build and publish docker images from a dockerfile. IMG
is used in place of the standard Docker toolchain to circumvent security restrictions within GitLab pipelines.

#### Customization

| Variable             	  | Description                                                                                                                 	          |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| DOCKER_DIRECTORY     	  | Declares the directory where the dockerfile is located. If not specified then the project's root directory will be searched 	          |
| DOCKER_REPO_USERNAME 	  | Username credentials for authentication used for the Docker registry that the image will be published to                             	 |
| DOCKER_REPO_PASSWORD 	  | Password credentials for authentication used for the Docker registry that the image will be published to                             	 |
| DOCKER_REPO_HOSTNAME 	  | The docker registry host to authenticate with.                                                                              	          |
| APP_NAME             	  | The unique identify that will be used as the tag for the docker image being built                                           	          |
| APP_VERSION          	  | The version used to tag the docker image being built                                                                        	          |
| PUBLISH_DOCKER        	 | Flag to manually publish a docker image from a GitLab pipeline on a non-default branch                           	                     |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/docker/Img.yml
```

---

### Playbook Deploy (job)

Deploys an Ansible Playbook.

#### Customization

| Variable              	        | Default Value                                                        	    | Description                                                                                                       	                          |
|--------------------------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| ANSIBLE_ROOT 	                 | ${CI_PROJECT_DIR}                                                 	       | The root directory of the Ansible project                                                                                                    |
| ANSIBLE_PLAYBOOK 	             | playbook.yml                                                 	            | The Ansible Playbook .yml file                                                                                                               |
| IMAGE_PREFIX 	                 | 	                                                                         | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job.                                                      |
| DEFAULT_IMAGE 	                | "python:3.11-rc-alpine"                                                 	 | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job. |
| ANSIBLE_CONFIG 	               | ./ansible.cfg                                                 	           | The Ansible .cfg file                                                                                                                        |
| ANSIBLE_LOG_PATH 	             | ~/ansible.log                                                	            | The Ansible .log file path                                                                                                                   |
| ANSIBLE_DEBUG 	                | "False"                                                 	                 | True to turn on Ansible debug                                                                                                                |
| ANSIBLE_PLAYBOOK_EXTRA_VARS 	  | 	                                                                         |                                                                                                                                              |
| BASE64_ENCODED_SSH_PRIVATE_KEY | 	                                                                         | The base 64 encoded SSH private key so Ansible can interact with the VM and it can be Gitlab masked                                          |
| SSH_PRIVATE_KEY_FILENAME 	     | 	                                                                         | The SSH private key filename so that Ansible can interact with the VM                                                                        |
| SERVER_HOST_IPS 	              | 	                                                                         | Known host IPs of the Azure VMs                                                                                                              |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/ansible/PlaybookDeploy.yml
```

### Checkov IaC SAST (job)

Uses the [Checkov](https://github.com/bridgecrewio/checkov) to create an Infrastructure as Code (IaC) Static Application
Security Testing (SAST) report.

#### Customization

| Variable          	         | Description                                                       	 |
|-----------------------------|---------------------------------------------------------------------|
| CHECKOV_OUTPUT_FILE    	    | The name of file to output the Checkov IaC SAST report to	          |
| CHECKOV_COMMAND 	           | The command to generate the Checkov IaC SAST report       	         |
| CHECKOV_IAC_SAST_DISABLED 	 | Used to disable the Checkov IaC SAST job from running       	       |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/security/CheckovIacSast.yml
```

---

### Trivy SBOM (job)

Uses the [Trivy](https://github.com/aquasecurity/trivy) to create a SBOM report.

#### Customization

| Variable          	     | Description                                                       	                     |
|-------------------------|-----------------------------------------------------------------------------------------|
| TRIVY_USERNAME 	        | The Docker registry username       	                                                    |
| TRIVY_PASSWORD    	     | The Docker registry password	                                                           |
| TRIVY_AUTH_URL 	        | The Docker registry url       	                                                         |
| TRIVY_SBOM_FLAGS    	   | Flags to call with trivy	                                                               |
| TRIVY_SBOM_FORMAT 	     | Format of trivy sbom       	                                                            |
| TRIVY_SBOM_TARGET    	  | Target for trivy to scan such as a Docker image or directory	                           |
| TRIVY_SBOM_OUTPUT 	     | Trivy sbom output file       	                                                          |
| TRIVY_SBOM_COMMAND    	 | Trivy command	                                                                          |
| TRIVY_SBOM_DISABLED 	   | Used to disable the Trivy SBOM job from running       	                                 |
| IMAGE_PREFIX            | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job. |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/security/Trivy.yml
```

---

### Fortify Security Scanning (job)

Uses Fortify to performance a security scan.

#### Customization

| Variable              	        | Description                                                                                                       	 |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------|
| JAVA_SRC_VERSION 	             | The java source version to scan                                                	                                    |
| PACKAGE_ENTRY_POINT        	   | Entry point to the Java package 	                                                                                   |
| DEFAULT_FORTIFY_IMAGE        	 | Fortify docker image                          	                                                                     |
| FORTIFY_EXCLUDE_FLAGS          | Source to exclude                                                                                                   |
| FORTIFY_RULES_FLAGS            | rules flags                                                                                                         |
| IMAGE_PREFIX                   | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job.                             |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/security/FortifyScanning.yml
```

---

### SonarQube Analysis (job)

Runs SonarQube gradle tasks to analyze a repo and publish generated reports to a SonarQube instance.

#### Customization

| Variable          	 | Description                                                       	 |
|---------------------|---------------------------------------------------------------------|
| SONAR_PROJECT_KEY 	 | The unique identifier of the project generated in SonarQube       	 |
| SONAR_HOST_URL    	 | The base SonarQube URL where analysis results are published 	       |
| SONAR_LOGIN_TOKEN 	 | An authentication token generated by SonarQube             	        |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gradle/SonarQube.yml
```

---

### Mega Linter (job)

Uses the [Mega Linter toolchain](https://github.com/oxsecurity/megalinter) to lint a repo.

#### Customization

| Variable          	       | Description                                                       	                     |
|---------------------------|-----------------------------------------------------------------------------------------|
| ENABLE 	                  | The types of lints to enable       	                                                    |
| FILTER_REGEX_EXCLUDE    	 | Files to exclude from linting	                                                          |
| MEGA_LINTER_DISABLED      | Used to disable the mega-linter job from running                                        |
| IMAGE_PREFIX              | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job. |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/lint/MegaLinter.yml
```

---

### Publish Helm Chart (jobs)

Runs a lint check to validate the integrity of the project's helm chart and subsequently publishes the helm chart to a
registry

#### Customization

| Variables                 	                 | Description                                                                          	    |
|---------------------------------------------|-------------------------------------------------------------------------------------------|
| PUBLISH_HELM_CHARTS_IMAGE 	                 | The docker image used to build and publish the helm chart                            	    |
| HELM_CHART_DIR            	                 | The path of the directory containing the helm chart                                  	    |
| CHART_PROJECT_NAME        	                 | The name that the helm chart will appear under in the chart registry                 	    |
| CHART_REPO_URL            	                 | The base URL of the chart registry excluding the group and project specific identifiers 	 |
| HELM_CHART_GPG_SIGN_KEY            	        | The GPG sign key name to sign the helm chart with during packaging 	                      |
| HELM_CHART_GPG_PASSPHRASE            	      | The passphrase for the GPG key to sign the helm chart with during packaging 	             |
| HELM_CHART_GPG_PASSPHRASE_FILE            	 | The file to write the passphrase to to then sign the helm chart with during packaging 	   |
| CHART_REPO_USERNAME           	             | Username for the chart repository to push to 	                                            |
| CHART_REPO_PASSWORD            	            | Password for the chart repository to push to 	                                            |
| CHART_REPO_OCI           	                  | Set to "true" if using an OCI registry for Helm like Harbor 2.7 or later 	                |
| OCI_CHART_ROOT            	                 | The project's root path to push helm charts to for a Helm 	                               |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/helm/PublishHelmChart.yml
```

### Trufflehog Secret Detection (job)

Runs Trufflehog to detect secrets in a Gitlab repository.

#### Customization

| Variables                 	 | Description                                                                          	                                               |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| TRUFFLEHOG_COMMAND 	        | The Trufflehog command you want to execute, see https://github.com/trufflesecurity/trufflehog for details                          	 |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/security/TrufflehogSecretDetection.yml
```

### Gitlab Release (job)

Creates a Gitlab Release that is viewable in a Gitlab repository's UI on the Release page that can include zipped source code, asset links, and more. See https://docs.gitlab.com/ee/user/project/releases/.

#### Customization

| Variables                 	              | Description                                                                          	                                                                                                                                                                                                                                                                                  |
|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GITLAB_RELEASE_TOKEN (REQUIRED)	         | Needs to be set to a Gitlab access token with at least api permissions                       	                                                                                                                                                                                                                                                                          |
| GITLAB_RELEASE_CLI_FLAGS 	               | The Gitlab Release CLI tool flags, see https://gitlab.com/gitlab-org/cli for details                          	                                                                                                                                                                                                                                                         |
| GITLAB_RELEASE_CLI_FLAGS_EXTRA_DYNAMIC 	 | Extra dynamic flags variable, not typical immutable Gitlab variable, for the Gitlab Release CLI tool that can be used to dynamically set things like assets-links using a previous Gitlab job with artifacts -> reports -> dotenv: variables.env, see https://docs.gitlab.com/ee/user/project/releases/release_cicd_examples.html for example                         	 |
| GITLAB_RELEASE_DISABLED 	                | Disabled by default, please set to "false" to enable the Gitlab Release job to run       	                                                                                                                                                                                                                                                                              |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/5/lib/gitlab/ci/templates/jobs/gitlab/GitlabRelease.yml
```

## Change log

[CHANGELOG.md](./CHANGELOG.md)

## Requirements

Current Gitlab version required is unknown, but one day we'll find out.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

[CONTRIBUTING.md](./CONTRIBUTING.md) and [CONTRIBUTORS.md](./CONTRIBUTORS.md)

## Release Process
If a major version breaking change occurs a release is needed. The release steps are:
1. Create a new release branch (e.g., `release/5`) from the previous release branch (e.g., `release/5`).
2. Create a branch (e.g., `feature/adds-something`) for the breaking changes.  
3. Update all code, such as `include` statements and `README.md` documentation, to use the new release branch. 
4. Create a merge request with the breaking changes into the new release branch. 
5. Merge once approvals given. 
6. At https://github.com/chesapeaketechnology/gitlab-templates/settings set the default branch to the newly created release branch.
7. Update all Golden Path examples, such as `include` statements in their .gitlab-ci.yml files` to use the newly created release branch. 

## License

[LICENSE.txt](./LICENSE.txt)
