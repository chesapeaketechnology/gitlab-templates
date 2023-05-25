# GitLab Pipeline Templates

GitLab Pipeline Templates is a collection of shared GitLab jobs and pipelines aimed at simplifying the process of setting up and maintaining the continuous integration tasks. These templates include tasks to run build scripts, unit tests, and to publish artifacts.

## Usage
### Versioning
It's important to understand that these templates are versioned by branches in GitLab to improve stability between changes. Non-latest release branches will only make additive changes and backwards compatible changes. The latest release-branch branch will always be updated with the latest changes which can cause your pipelines to break.

### Getting Started
Inside the root directory of your project, create a file named `.gitlab-ci.yml` and copy the content from the section(s) below that most closely match your needs. Multiple include statements can be combined to capture all the jobs that you want to capture in your pipeline. 

### Gradle Java Pipeline
The standard gradle pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will build, test, and publish jars from a project utilizing the [Build Support Plugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.build-support)(BSP). By default, snapshots are published whenever a branch is merged into the "default" branch. Release jars are only created when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below) from a branch match the below DEV_OR_RELEASE_REGEX variable. 

#### Linked Jobs
- [Secrets Detection](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Secret-Detection.gitlab-ci.yml)
- [Dependency Scanning](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Dependency-Scanning.gitlab-ci.yml)
- [SAST](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST.gitlab-ci.yml)
- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)
- [Test](#gradle-test-job)
- [Publish Jar](#publish-jar-job)
- [Fortify Security Scanning](#fortify-security-scanning-job)
- [Publish Pages](#publish-pages-job)
- [Secrets Detection](#secrets-detection-job)
- [Quality Reporting](#quality-reporting-job)
- [Dependency Scanning](#dependency-scanning-jobs)
- [License Scanning](#license-scanning-job)
- [SAST](#sast-jobs)
- [AsciiDoc](#asciidoc-job)
  

#### Customization
| Variable                                     | Pre-Loaded** | Default Value                                                        	              | Description                                                                                                                                            	                                                     |
|----------------------------------------------|--------------|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEFAULT_IMAGE           	                    | &check;      | openjdk:11                                                                          | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	                                                     |
| IMAGE_PREFIX                 	               |              | 	                                                                                   | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                                                                           |
| BASE_GRADLE_FLAGS   	                        | &check;      | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest)	 | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true")                                                                                  |
| EXTRA_GRADLE_FLAGS                 	         | &check;      | 	                                                                                   | Any extra gradle flags. 	                                                                                                                                                                                    |
| DEV_REGEX                                    | &check;      | `^develop$`\|`^v3-develop$`\|`^v2-develop$`                                         | Branch(es) jobs will be run from when new commits are made. For example, if it's desired to run jobs from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\|$^v2-develop$'` |
| RELEASE_REGEX                                | &check;      | `^[0-9]+\.[0-9]+$\|^release\/.+$`                                                   | Release oriented jobs will be run based on this regex.                                                                                                                                                       | 
| DEV_OR_RELEASE_REGEX                         | &check;      | `$DEV_REGEX\|$RELEASE_REGEX`                                                        | Dev and release oriented jobs will be run based on this regex.                                                                                                                                               |
| SAFE_TEST                                    | &check;      | false                                                                               | Boolean on whether to run the build pipeline as a test before actually deploying, when set to \"true\" the build will not publish or deploy and artifacts.                                                   |
| TASK_ARGUMENTS                               |              |                                                                                     | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.                                                     |
| RELEASE                 	                    | &check;      | 	                                                                                   | The name that will be appended to release build artifacts. By default an release candidate will be created from this unless the value "final" is used. 	                                                     |
| GRADLE_TEST_FLAGS                 	          | &check;      | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	              | Gradle flags that will be appended when running the Test Gradle task(s). 	                                                                                                                                   |
| QUALITY_CHECK_GRADLE_TASKS                 	 | &check;      | pmdMain violations -x build -x test	                                                | The gradle tasks used to run the Quality Check Gradle task(s). 	                                                                                                                                             |
| QUALITY_CHECK_DISABLED                 	     | &check;      | true	                                                                               | Boolean on whether to run the Quality Check Gitlab job(s).  	                                                                                                                                                |
| DEPENDENCY_LICENSE_SCANNING_DISABLED         | &check;      | true	                                                                               | Boolean on whether to run the Dependency License Scan Gitlab job(s).  	                                                                                                                                      |
| SAST_DISABLED                 	              | &check;      | true	                                                                               | Boolean on whether to run the SAST Gitlab job(s).  	                                                                                                                                                         |
| FORTIFY_SCANNING_DISABLED                 	  | &check;      | true	                                                                               | Boolean on whether to run the Fortify Gitlab job(s).  	                                                                                                                                                      |
| ASCIIDOC_DISABLED                 	          | &check;      | true	                                                                               | Boolean on whether to run the AsciiDoc Gitlab job(s).  	                                                                                                                                                     |
| ASCIIDOC_GRADLE_TASKS                 	      | &check;      | createDocsDistributionZip	                                                          | The gradle tasks used to run the AsciiDoc Gradle task(s).  	                                                                                                                                                 |

** Denotes Gitlab Pipeline runner will have these variables present when manually building.
#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/GradleJavaPipeline.yml
```

---

### Gradle Android Pipeline
The Gradle Android pipeline provides basic jobs for building Android APKs. When APKs are built with the Gitlab pipeline they are posted to a Slack channel. 

#### Linked Jobs
- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)

#### Customization
| Variable                           | Pre-Loaded** | Default Value                                                        	                                                     | Description                                                                                                                                            	 |
|------------------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEFAULT_IMAGE           	          | &check;      | jangrewe/gitlab-ci-android                                                                                                 | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	 |
| IMAGE_PREFIX                 	     |              | 	                                                                                                                          | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                       |
| DEPLOY_DEBUG_APK_SLACK_MESSAGE   	 | &check;      | "Hello Team! Here is the latest debug APK from branch ${CI_COMMIT_REF_NAME}. It was triggered by: ${CI_PIPELINE_SOURCE}."	 | The Slack message to to send in the Slack message                                                                                                        |
| DEPLOY_DEBUG_APK_PATH              | &check;      | `app/build/outputs/apk/debug`                                                                                              | The directory path to the debug apk                                                                                                                      |
| DEPLOY_DEBUG_APK_NAME              | &check;      | "yourdebugapkname"                                                                                                         | The name of the debug apk                                                                                                                                | 
| APK_SLACK_CHANNEL_ACCESS_TOKEN     | &check;      |                                                                                                                            | The Slack channel access token                                                                                                                           |
| APK_SLACK_CHANNEL_ID               | &check;      |                                                                                                                            | The Slack channel access ID                                                                                                                              |

** Denotes Gitlab Pipeline runner will have these variables present when manually building.
#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/AndroidTemplate.yml
```

---

### Gradle ATAK Build Support Plugin (BSP) Pipeline
The Gradle ATAK Build Support Plugin (BSP) pipeline provides basic jobs for building ATAK APKs with [BSP](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.build-support). APKs are published by default whenever a branch is merged into the "default" branch.

#### Linked Jobs
- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)

#### Customization
| Variable                             | Pre-Loaded** | Default Value                                                        	 | Description                                                                                                                                            	                                     |
|--------------------------------------|--------------|------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RELEASE                 	            | &check;      | 	                                                                      | The name that will be appended to release build artifacts. By default an release candidate will be created from this unless the value "final" is used. 	                                     |
| EXTRA_GRADLE_FLAGS                 	 | &check;      | 	                                                                      | Any extra gradle flags	                                                                                                                                                                      |
| STANDARD_GRADLE_FLAGS   	            | &check;      | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain	  | Default Gradle flags that will be appended to all Gradle commands                                                                                                                            |
| DEV_REGEX                            | &check;      | `^develop$`\|`^v3-develop$`\|`^v2-develop$`                            | Branch(es) jobs will be run from when new commits are made. For example, if it's desired to run jobs from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\ |$^v2-develop$'`
| RELEASE_REGEX                        | &check;      | `^[0-9]+\.[0-9]+$\|^release\/.+$`                                      | Release oriented jobs will be run based on this regex.                                                                                                                                       | 
| SUPPORT_REGEX                        | &check;      | `^[0-9]+\.[0-9]+$\|^support\/.+$`                                      | Support oriented jobs will be run based on this regex.                                                                                                                                       | 
| DEV_OR_RELEASE_OR_SUPPORT_REGEX      | &check;      | `$DEV_REGEX\|$RELEASE_REGEX\|$SUPPORT_REGEX`                           | Dev, release, and support oriented jobs will be run based on this regex.                                                                                                                     | 
| DEFAULT_IMAGE           	            | &check;      | jangrewe/gitlab-ci-android                                             | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	                                     |
| IMAGE_PREFIX                 	       |              | 	                                                                      | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                                                           |
| REPORTS_ARTIFACT                     | &check;      | ${CI_PROJECT_DIR}/app/build/reports/tests/                             | The test artifact on the build job, typically the unit test report                                                                                                                           | 
** Denotes Gitlab Pipeline runner will have these variables present when manually building.
#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/AndroidTemplateExt.yml
```

---

### Gradle Install4J Pipeline
The gradle Install4j pipeline provides basic jobs for building installers using the [InstallerSupportPlugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.installer-support). The default jobs provided allow projects to create both SNAPSHOT and RELEASE installers. SNAPSHOTS are published by default whenever a branch is merged into the "default" branch. Release installers are only created when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below) from a branch matching the DEV_OR_RELEASE_REGEX variable.

#### Customization
| Variable 	                           | Default Value 	                                                                    | Description 	                                                                                                                                                                                      |
|--------------------------------------|------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEFAULT_INSTALL4J_IMAGE 	            | devsecops/install4j8:1.0.0-jdk11-slim-custom 	                                     | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job. 	                                                     |
| INSTALLER_ARTIFACT_PATH 	            | build/installers 	                                                                 | The path relative to the root of the project where the build artifacts can be found. 	                                                                                                             |
| INSTALLER_NAME 	                     | "installers"	                                                                      | The name of the installer artifacts that can be downloaded after the job completes 	                                                                                                               |
| INSTALLER_GRADLE_COMMANDS 	          | makeAllInstallers makeAllBundles 	                                                 | Gradle commands that determine which installers should be built. If building a project with multiple installers, override this variable to build a specific installer instead of all installers. 	 |
| EXTRA_GRADLE_FLAGS                 	 |                                                                                    | Any extra gradle flags                                                                                                                                                                             |
| STANDARD_GRADLE_FLAGS   	            | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest) | Default Gradle flags that will be appended to all Gradle commands 	                                                                                                                                | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |
| INSTALL4J_VERSION 	                  | unix_8_0_11 	                                                                      | The version of Install4J used to build the installers. 	                                                                                                                                           |
| RELEASE                 	            |                                                                                    | 	                                                                                                                                                                                                  | The name that will be appended to release build artifacts. By default an release candidate will be created from this unless the value "final" is used. 	                                     |
| DEV_OR_RELEASE_REGEX 	               | `^develop$\|^[0-9]+\.[0-9]+$\|^release\/.+$ \|^support\/.+$                        | Dev and release oriented jobs will be run based on this regex.	                                                                                                                                    | Regular expression used to evaluate whether publishing should be enabled. If the pattern matches the branch name, then snapshot and release artifacts will be published.  	|
| JDK_SELECTOR 	                       | -PJDK=11 	                                                                         | Flag that specifies which Java version the installer should target. 	                                                                                                                              |



#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/GradleInstall4JPipeline.yml
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
| DEFAULT_IMAGE         | openjdk:8-jdk-slim                                                                   | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.             |
| STANDARD_GRADLE_FLAGS | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain $TASK_ARGUMENTS | Default Gradle flags that will be appended to all Gradle commands                                                                                        |
| TASK_ARGUMENTS        |                                                                                      | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream. |
| RELEASE               | 'false'                                                                              | Determines if a 'release' build will be performed, which also publishes the plugin to the Gradle Plugin Portal.  Use 'true' to perform a release build.  |
| GRADLE_PUBLISH_KEY    | NONE                                                                                 | The Gradle plugin portal publishing key, must be set as an environment variable                                                                          |
| GRADLE_PUBLISH_SECRET | NONE                                                                                 | The Gradle plugin portal publishing secret, must be set as an environment variable                                                                       |


#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/GradlePluginReleasePipeline.yml
```

---

### Packer Pipeline
The standard Packer pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will format, validate, and deploy Packer VMs from a project. 

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/PackerPipeline.yml
```

---

### NPM Jest Coverage Pipeline
The NPM pipeline provides basic jobs for building NPM packages.

#### Customization
| Variable                       | Pre-Loaded** | Default Value                                                        	 | Description                                                                                                                                            	 |
|--------------------------------|--------------|------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| NODE_IMAGE           	         | &check;      | node:16                                                                | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.           	                            |
| IMAGE_PREFIX                 	 |              | 	                                                                      | The Node Docker image to use in the Gitlab pipeline jobs.	                                                                                               |
| TEST_ARGS   	                  |              | 	                                                                      | Extra NPM test arguments                                                                                                                                 |

** Denotes Gitlab Pipeline runner will have these variables present when manually building.
#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/NpmJestCoveragePipeline.yml
```

---

### Webtak Test Coverage Pipeline
The WebTAK pipeline provides basic jobs for building WebTAK packages.

#### Linked Pipelines
- [NPM Jest Coverage Pipeline](#npm-jest-coverage-pipeline)

** Denotes Gitlab Pipeline runner will have these variables present when manually building.
#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/WebtakTestCoverage.yml
```

---
### Terraform Pipeline
The standard Terraform pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will format, validate, security test, plan, apply, and destroy Terraform Infrastructure as Code (IaC) from a project. Can be used for any cloud environment (e.g., Azure, AWS, etc).

#### Linked Jobs
- [Checkov IaC SAST](#checkov-iac-sast-job)

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/TerraformPipeline.yml
```

---

### Docker Pipeline
The standard Docker pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will lint and apply Docker continuous deployments (CD) from a project. 

#### Linked Jobs
- [Mega Linter](#mega-linter-job)
- [Kaniko Docker Image Publishing](#kaniko-docker-image-publishing-job)
- [Container Scanning](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/Container-Scanning.gitlab-ci.yml)
- [SAST IaC](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST-IaC.gitlab-ci.yml)
- [Trivy SBOM](#trivy-sbom-job)
- [Checkov IaC SAST](#checkov-iac-sast-job)

#### Customization
| Variable                       | Description                                                	                                                                                                                                          |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| USE_DOCKER_AUTH_CONFIG         | Defaults to "true", "true" is for using a `DOCKER_AUTH_CONFIG` for Kaniko authentication, use "false" to authenticate with `DOCKER_REPO_HOSTNAME`, `DOCKER_REPO_USERNAME`, and `DOCKER_REPO_PASSWORD` |
| DOCKER_DIRECTORY               | Optional variable to set the directory where the Dockerfile is located                                                                                                                                |
| DOCKERFILE                     | Optional variable to set the name of the Dockerfile (e.g., Dockerfile.mine)                                                                                                                           |
| DOCKER_REPO_USERNAME           | Username to publish the Docker image                                                                                                                                                                  |
| DOCKER_REPO_PASSWORD           | Password to publish the Docker image                                                                                                                                                                  |
| DOCKER_REPO_HOSTNAME           | Docker repository hostname (e.g., docker-custom-local.artifacts.net)                                                                                                                                  |
| DOCKER_REPO_NAME               | Docker repository name (e.g., devsecops)                                                                                                                                                              |
| APP_NAME                       | Docker image app name (e.g., MyCustomKafka)                                                                                                                                                           |
| VERSION                        | Docker image version (e.g., latest)                                                                                                                                                                   |
| IMAGE_PREFIX                 	 |                                                                                                                                                                                                       | 	                                                                                                                          | Adds a prefix to the Docker images used to run the Gitlab jobs. Useful for when using non Dockerhub repositories.	                                       |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/DockerPipeline.yml
```

---

### Helm Pipeline
The standard Helm pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will lint and apply Helm continuous deployments (CD) from a project.

#### Linked Jobs
- [Mega Linter](#mega-linter-job)
- [Publish Helm Chart Jobs](#publish-helm-chart-jobs)
- [Checkov IaC SAST](#checkov-iac-sast-job)

#### Customization
| Variable     | Description                                                	                            |
|--------------|-----------------------------------------------------------------------------------------|
| IMAGE_PREFIX | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job. |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/HelmPipeline.yml
```

---

### Ansible Pipeline
The standard Ansible pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will lint and apply Ansible continuous deployments (CD) from a project. Can be used for any virtual machine host (e.g., Azure VMs, AWS VMs, local VMs, etc).

#### Linked Jobs
- [Mega Linter](#mega-linter-job)
- [SAST IaC](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Jobs/SAST-IaC.gitlab-ci.yml)
- [Checkov IaC SAST](#checkov-iac-sast-job)
- [Playbook Deploy](#playbook-deploy-job)

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/AnsiblePipeline.yml
```

---

### NPM Unit Test and Test Coverage Pipeline
The standard NPM pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will install, build, test, and provide test results and coverage reports on both merge requests and gitlab pages.

#### Requirements
The pipeline expects a `package.json` script called `test:ci`. It's recommended to follow the below setup to ensure this pipeline works as expected.

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

| Variable   | Description                                                	               |
|------------|----------------------------------------------------------------------------|
| NODE_IMAGE | The base node image used to run all jobs. (e.g. node:16)          	        |
| TEST_ARGS  | Optional additional arguments or flags to add to the `npm test:ci` script. |

#### Reference URL

```
include:
    - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/NpmJestCoveragePipeline.yml

```

---

### WebTAK Plugin Test Coverage Pipeline

The standard NPM pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration
that will install, build, test, and provide test results and coverage reports on both merge requests and gitlab pages.

#### Requirements

The pipeline has this repo's `NpmJestCoveragePipeline` as an included dependency. It is necessary to follow the
requirements from that pipeline in order to use this one.

#### Customization

| Variable      | Description                                                                           |
|---------------|---------------------------------------------------------------------------------------|
| TAK_EMAIL     | A valid TAK.gov email account with access to WebTAK artifacts on the TAK Artifactory. |
| TAK_API_TOKEN | An API token generated using the same email as above.                                 |

#### Reference URL

```
include:
    - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/pipeline/WebtakTestCoverage.yml

```

---

### Gradle Wrapper Configuration (job)

Enables caching in GitLab to reuse the gradle wrapper between jobs and gives the gradle wrapper executable file permissions.

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/references/gradle/GradleWrapperSetup.yml
```

---

### Gradle Test (job)

Runs tests through Gradle commands and publishes the results as an artifact to GitLab. These test result artifacts can be viewed by going to your project's CI pipelines page and then selecting the context menu on the right hand of the test job.

#### GitLab Artifacts
- Tests results found in the build/test-results/test/ directory. This is the default location for JUnit test results.

#### Customization

| Variable          	       | Description                                            	 |
|---------------------------|----------------------------------------------------------|
| EXTRA_GRADLE_TEST_FLAGS 	 | Flags that will be appended to the gradle test command 	 |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/Test.yml
```

---

### Publish Jar (job)
Publishes a SNAPSHOT jar whenever a feature branch is merged into the project's default branch and publishes release jars when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below). After performing a release build, the project's version is automatically updated and the change is committed to the repo. Javadocs are also published with releases.

#### Customization

| Variable                	     | Default Value                                                        	             | Description                                                                                                                                                                               	                          |
|-------------------------------|------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| STANDARD_GRADLE_FLAGS   	     | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest) | Default Gradle flags that will be appended to all Gradle commands  	                                                                                                                                                 | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |
| PUBLISH_SNAPSHOT_GRADLE_FLAGS | 	                                                                                  | Gradle flags for customizing the snapshot & release publish tasks                                                                                                                                                    |
| RELEASE_GRADLE_FLAGS          | -x updateReleaseVersion -x tagRelease                                              | Flags passed to the gradle command used to publish release jars.                                                                                                                                                     |
| GIT_TASKS_ENABLED             | true                                                                               | Determines whether any gradle tasks that perform Git operations with be included in the pipeline. If disabled a project's version will not be automatically updated following a release build                        |
| DEV_REGEX                     | develop                                                                            | Branch(es) SNAPSHOT builds will be published from when new commits are made. For example, if it's desired to build SNAPSHOTs from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\ |$^v2-develop$'` |
| SAFE_TEST                     | false                                                                              | Boolean on whether to run the build pipeline as a test before actually deploying, when set to \"true\" the build will not publish or deploy and artifacts.                                                           |
| TASK_ARGUMENTS                |                                                                                    | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.                                                             |
| RELEASE                 	     | 	                                                                                  | The name that will be appended to release build artifacts. By default a release candidate will be created from this unless the value "final" is used   	                                                             |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/PublishJar.yml
```

---

### Publish Pages (job)
Publishes Gitlab Pages such as JavaDocs, coverage, quality, licenses, and vulnerabilities.

#### Customization

| Variable                	   | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|-----------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FORCE_PUBLISH_PAGES   	     |                                                                        | True to force publishing of pages.  	                                                                                                                                                       | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |
| PUBLISH_JAVADOCS_DISABLED   | 	                                                                      | True to disable JavaDoc publishing.                                                                                                                                                         |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/PublishPages.yml
```

---

### Secrets Detection (job)
Gradle job to detect secrets and put into a report.

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/SecretDetection.yml
```

---

### Quality Reporting (job)
Gradle job to scan quality and put into a report.

#### Customization

| Variable                	  | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|----------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| QUALITY_CHECK_DISABLED   	 |                                                                        | True to disable quality reporting.  	                                                                                                                                                       | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/QualityReporting.yml
```

---

### Dependency Scanning (jobs)
Jobs to scan dependency vulnerabilities of Gradle projects and put into a report.

#### Customization

| Variable                	    | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MAVEN_DETECTION_DISABLED   	 |                                                                        | True to disable dependency scanning.  	                                                                                                                                                     | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/DependencyScanning.yml
```

---
### SAST (jobs)
Static Application Security Testing (SAST) scanning and reports for a Gradle project.

#### Customization

| Variable                	 | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|---------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ASDF_JAVA_VERSION   	     | adoptopenjdk-17.0.1+12                                                 | The ASDF Java version.  	                                                                                                                                                                   | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |
| SAST_DISABLED   	         |                                                                        | True to disable the jobs.  	                                                                                                                                                                | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/StaticApplicationSecurityTesting.yml
```

---

### License Scanning (job)
Jobs to scan licenses of Gradle projects and put into a report.

#### Customization

| Variable                	                | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DEPENDENCY_LICENSE_SCANNING_DISABLED   	 |                                                                        | True to disable license scanning.  	                                                                                                                                                        | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/LicenseScanning.yml
```

---

### Asciidoc (job)
Creates AsciiDoc using a Gradle job using the [AsciiDoc Generator Gradle Plugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.asciidoc-generator).

#### Customization

| Variable                	 | Default Value                                                        	 | Description                                                                                                                                                                               	 |
|---------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ASCIIDOC_GRADLE_TASKS   	 |                                                                        | The AsciiDoc Gradle tasks.  	                                                                                                                                                               | Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/Asciidoc.yml
```

---

### Kaniko Docker Image Publishing (job)
Uses the gradle [Kaniko Docker image](https://github.com/GoogleContainerTools/kaniko) to build and publish docker images.

#### Customization

| Variable              	  | Default Value                                                        	                                                                       | Description                                                                                                       	 |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| USE_DOCKER_AUTH_CONFIG 	 | Default Gradle flags that will be appended to all Gradle commands                                                 	                          |
| DOCKER_DIRECTORY         | Gradle flags used to customize the JIB task. The default value enables publishing docker images to insecure registries 	                     |
| DOCKERFILE               | Flag to manually publish a docker image from a GitLab pipeline on a non-default branch                           	                           |
| DOCKER_AUTH_CONFIG       | A config with the repo, username, and password, see https://docs.gitlab.com/ee/ci/docker/using_kaniko.html for more details of config format |       
| DOCKER_REPO_HOSTNAME     | Only needed if not using DOCKER_AUTH_CONFIG. URL to docker repository, i.e. `harbor.ctic-dev.com`                                            |       
| DOCKER_REPO_USERNAME     | Only needed if not using DOCKER_AUTH_CONFIG. Username for that repository                                                                    |
| DOCKER_REPO_PASSWORD     | Only needed if not using DOCKER_AUTH_CONFIG. Password for that repository                                                                    | 
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/docker/Kaniko.yml
```

---

### JIB Docker Image Publishing(job)
Uses the gradle [JIB Gradle plugin](https://github.com/GoogleContainerTools/jib/tree/master/jib-gradle-plugin) to build and publish docker images. The
job will attempt to use your credentials stored in the `$HOME/.docker/config.json` file on the Gitlab instance running the pipeline. If the `HOME` variable
is not set or the credentials are not present on your system, use the username and password variables detailed below. 

> Note: Be sure NOT to save credentials directly to your code repository. 
> 
> Note: This job will only run when code is committed to the repository's default branch, i.e. it will not run in merge requests, and will 
> instead run after the request is merged. 

#### Customization

| Variable              	 | Default Value                                                        	 | Description                                                                                                       	      |
|-------------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| STANDARD_GRADLE_FLAGS 	 | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	 | Default Gradle flags that will be appended to all Gradle commands                                                 	      |
| JIB_FLAGS             	 | -DsendCredentialsOverHttp=true                                       	 | Gradle flags used to customize the JIB task. The default value enables publishing docker images to insecure registries 	 |
| PUBLISH_DOCKER        	 | 	                                                                      | Flag to manually publish a docker image from a GitLab pipeline on a non-default branch                           	       |
| DOCKER_REPO_HOSTNAME    |                                                                        | URL to docker repository, i.e. `harbor.ctic-dev.com`                                                                     |       
| DOCKER_REPO_USERNAME    |                                                                        | Username for that repository                                                                                             |
| DOCKER_REPO_PASSWORD    |                                                                        | Password for that repository                                                                                             | 
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/docker/Jib.yml
```

---

### IMG Docker Image Publishing (job)
Uses the [IMG toolchain](https://github.com/genuinetools/img) to build and publish docker images from a dockerfile. IMG is used in place of the standard Docker toolchain to circumvent security restrictions within GitLab pipelines.

#### Customization

| Variable             	 | Description                                                                                                                 	          |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| DOCKER_DIRECTORY     	 | Declares the directory where the dockerfile is located. If not specified then the project's root directory will be searched 	          |
| DOCKER_REPO_USERNAME 	 | Username credentials for authentication used for the Docker registry that the image will be published to                             	 |
| DOCKER_REPO_PASSWORD 	 | Password credentials for authentication used for the Docker registry that the image will be published to                             	 |
| DOCKER_REPO_HOSTNAME 	 | The docker registry host to authenticate with.                                                                              	          |
| APP_NAME             	 | The unique identify that will be used as the tag for the docker image being built                                           	          |
| APP_VERSION          	 | The version used to tag the docker image being built                                                                        	          |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/docker/Img.yml
```

---

### Playbook Deploy (job)
Deploys an Ansible Playbook.

#### Customization

| Variable              	       | Default Value                                                        	    | Description                                                                                                       	                          |
|-------------------------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| ANSIBLE_ROOT 	                | ${CI_PROJECT_DIR}                                                 	       | The root directory of the Ansible project                                                                                                    | 
| ANSIBLE_PLAYBOOK 	            | playbook.yml                                                 	            | The Ansible Playbook .yml file                                                                                                               | 
| IMAGE_PREFIX 	                | 	                                                                         | Used to add an image prefix at the beginning of an image used by a Gitlab pipeline job.                                                      | 
| DEFAULT_IMAGE 	               | "python:3.11-rc-alpine"                                                 	 | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job. | 
| ANSIBLE_CONFIG 	              | ./ansible.cfg                                                 	           | The Ansible .cfg file                                                                                                                        | 
| ANSIBLE_LOG_PATH 	            | ~/ansible.log                                                	            | The Ansible .log file path                                                                                                                   | 
| ANSIBLE_DEBUG 	               | "True"                                                 	                  | True to turn on Ansible debug                                                                                                                | 
| ANSIBLE_PLAYBOOK_EXTRA_VARS 	 | 	                                                                         |                                                                                                                                              | 
| SSH_PRIVATE_KEY 	             | 	                                                                         | The SSH private key so Ansible can interact with the VM                                                                                      | 
| SSH_PRIVATE_KEY_FILENAME 	    | 	                                                                         | The SSH private key filename so that Ansible can interact with the VM                                                                        | 
| SERVER_HOST_IPS 	             | 	                                                                         | Known host IPs of the Azure VMs                                                                                                              | 

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/ansible/PlaybookDeploy.yml
```

### Checkov IaC SAST (job)
Uses the [Checkov](https://github.com/bridgecrewio/checkov) to create an Infrastructure as Code (IaC) Static Application Security Testing (SAST) report.

#### Customization

| Variable          	         | Description                                                       	 |
|-----------------------------|---------------------------------------------------------------------|
| CHECKOV_OUTPUT_FILE    	    | The name of file to output the Checkov IaC SAST report to	          |
| CHECKOV_COMMAND 	           | The command to generate the Checkov IaC SAST report       	         |
| CHECKOV_IAC_SAST_DISABLED 	 | Used to disable the Checkov IaC SAST job from running       	       |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/security/CheckovIacSast.yml
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
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/security/Trivy.yml
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
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/security/FortifyScanning.yml
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
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/gradle/SonarQube.yml
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
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/lint/MegaLinter.yml
```

---

### Publish Helm Chart (jobs)
Runs a lint check to validate the integrity of the project's helm chart and subsequently publishes the helm chart to a registry 

#### Customization

| Variables                 	 | Description                                                                          	    |
|-----------------------------|-------------------------------------------------------------------------------------------|
| PUBLISH_HELM_CHARTS_IMAGE 	 | The docker image used to build and publish the helm chart                            	    |
| HELM_CHART                	 | The file descriptor of the zip file containing the helm chart's contents             	    |
| HELM_CHART_DIR            	 | The path of the directory containing the helm chart                                  	    |
| CHART_REPO_NAME           	 | The name of the group that the helm chart will be added to                           	    |
| CHART_PROJECT_NAME        	 | The name that the helm chart will appear under in the chart registry                 	    |
| CHART_REPO_URL            	 | The base URL of the chart registry excluding the group and project specific identifiers 	 |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.3/lib/gitlab/ci/templates/jobs/helm/PublishHelmChart.yml
```

## Change log

#### [1.2.0] on 2022-09-15 : Official stable release with many changes

#### [1.1.0] on 2021-11-7 : Updated docker `jib` job to take credentials as an argument if config file is not present

#### [1.0.0] on 2021-06-20 : Initial migration and publication of templates to a public repo for shared usage across GitLab instances
- Initial release mirroring the capabilities pulled from existing standardized pipelines used at CTI.

## Requirements
Current Gitlab version required is unknown, but one day we'll find out. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[Apache](http://www.apache.org/licenses/)
