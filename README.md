# GitLab Pipeline Templates

GitLab Pipeline Templates is a collection of shared GitLab jobs and pipelines aimed at simplifying the process of setting up and maintaining the continuous integration tasks. These templates include tasks to run build scripts, unit tests, and to publish artifacts.

## Usage
### Versioning
It's important to understand that these templates are versioned by branches in GitLab to improve stability between changes. Release branches will only make additive changes and backwards compatible changes. The master branch will always be updated with the latest changes which can cause your pipelines to break. For this reason it is **not** recommended to depend directly on the master branch when using these templates.

### Getting Started
Inside the root directory of your project, create a file named `.gitlab-ci.yml` and copy the content from the section(s) below that most closely match your needs. Multiple include statements can be combined to capture all of the jobs that you want to capture in your pipeline. 

### Gradle Java Pipeline
The standard gradle pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will build, test, and publish jars from a project. By default, SNAPSHOTS are published whenever a branch is merged into the "default" branch. Release jars are only created when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below) from a branch following the naming convention `feature/{version}`. 

#### Linked Jobs
- [Certificate of Authority Configuration](#certificate-of-authority-configuration-job)
- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)
- [Test](#gradle-test-job)
- [Publish Jar](#publish-jar-job)

#### Customization
| Variable                  | Pre-Loaded**| Default Value                                                        	                | Description                                                                                                                                            	|
|-----------------------	|-----------|-----------------------------------------------------------------------------------	|--------------------------------------------------------------------------------------------------------------------------------------------------------	|
| DEFAULT IMAGE           	|           | openjdk:11                                                                            | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	|
| STANDARD_GRADLE_FLAGS   	|           | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest)	| Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |
| DEV_REGEX                 |           | develop                                                                               | Branch(es) jobs will be run from when new commits are made. For example, if it's desired to run jobs from from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\|$^v2-develop$'`
| SAFE_TEST                 |&check;    | false                                                                                 | Boolean on whether to run the build pipeline as a test before actually deploying, when set to \"true\" the build will not publish or deploy and artifacts.|
| TASK_ARGUMENTS            |&check;    |                                                                                       | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.  |
| RELEASE                 	|&check;    |                                                                      	                | The name that will be appended to release build artifacts. By default an release candidate will be created from this unless the value "final" is used. 	|

** Denotes Gitlab Pipeline runner will have these variables present when manually building.
#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.1/lib/gitlab/ci/templates/pipeline/GradleJavaPipeline.yml
```

---

### Gradle Install4J Pipeline
The gradle Install4j pipeline provides basic jobs for building installers using the [InstallerSupportPlugin](https://plugins.gradle.org/plugin/gov.raptor.gradle.plugins.installer-support). The default jobs provided allow projects to create both SNAPSHOT and RELEASE installers. SNAPSHOTS are published by default whenever a branch is merged into the "default" branch. Release installers are only created when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below) from a branch following the naming convention `release/{version}`.

#### Customization
| Variable 	| Default Value 	| Description 	|
|---	|---	|---	|
| DEFAULT_INSTALL4J_IMAGE 	| devsecops/install4j8:1.0.0-jdk11-slim-custom 	| The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job. 	|
| INSTALLER_ARTIFACT_PATH 	| build/installers 	| The path relative to the root of the project where the build artifacts can be found. 	|
| INSTALLER_GRADE_COMMANDS 	| makeAllInstallers makeAllBundles 	| Gradle commands that determine which installers should be built. If building a project with multiple installers, override this variable to build a specific installer instead of all installers. 	|
| STANDARD_GRADLE_FLAGS   	|           | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest)	| Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |
| INSTALL4J_VERSION 	| unix_8_0_11 	| The version of Install4J used to build the installers. 	|
| DEV_OR_RELEASE_REGEX 	| '^develop$\|^[0-9]+\.[0-9]+$\|^release\/.+$' 	| Regular expression used to evaluate whether publishing should be enabled. If the pattern matches the branch name, then snapshot and release artifacts will be published.  	|
| JDK_SELECTOR 	| -PJDK=11 	| Flag that specifies which Java version the installer should target. 	|
| SAFE_TEST     | false     | Boolean on whether to run the build pipeline as a test before actually deploying, when set to \"true\" the build will not publish or deploy and artifacts.|
| TASK_ARGUMENTS    |       | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.                                               |
| RELEASE 	|  	| Set to "FINAL" when manually running the pipeline to create a release artifact instead of a snapshot. 	|

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.1/lib/gitlab/ci/templates/pipeline/GradleInstall4JPipeline.yml
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
| Variable 	| Default Value 	| Description 	|
|---	|---	|---	|
| DEFAULT IMAGE | openjdk:8-jdk-slim | The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job. |
| STANDARD_GRADLE_FLAGS | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain $TASK_ARGUMENTS | Default Gradle flags that will be appended to all Gradle commands |
| TASK_ARGUMENTS |  | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.  |
| RELEASE | 'false' | Determines if a 'release' build will be performed, which also publishes the plugin to the Gradle Plugin Portal.  Use 'true' to perform a release build. |
| GRADLE_PUBLISH_KEY | NONE | The Gradle plugin portal publishing key, must be set as an environment variable |
| GRADLE_PUBLISH_SECRET | NONE | The Gradle plugin portal publishing secret, must be set as an environment variable |


#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.2/lib/gitlab/ci/templates/pipeline/GradlePluginReleasePipeline.yml
```

---

### Packer Pipeline
The standard Packer pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will format, validate, and deploy Packer VMs from a project. 

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.1/lib/gitlab/ci/templates/pipeline/PackerPipeline.yml
```

---

### Terraform Pipeline
The standard Terraform pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will format, validate, security test, plan, apply, and destroy Terraform Infrastructure as Code (IaC) from a project. Can be used for any cloud environment (e.g., Azure, AWS, etc).

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.2/lib/gitlab/ci/templates/pipeline/TerraformPipeline.yml
```

---

### Ansible Pipeline
The standard Ansible pipeline is the simplest way to get up and running quickly. It provides a full pipeline configuration that will lint and apply Ansible continuous deployments (CD) from a project. Can be used for any virtual machine host (e.g., Azure VMs, AWS VMs, local VMs, etc).

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.2/lib/gitlab/ci/templates/pipeline/AnsiblePipeline.yml
```

---

### Certificate of Authority Configuration (job)

Adds a certificate of authority to a JDK's truststore to enable pulling & pushing artifacts in private Nexus repositories. If the environment variables below are not defined then this script do nothing.

#### Customization

| Variable    	| Description                                                	|
|-------------	|------------------------------------------------------------	|
| CERT_INT_AD 	| The name of internal active directory certificate          	|
| CERT_ROOT   	| The name of ECC SSL certificate                            	|
| CERT_HOST   	| The base URL where the certificates can be downloaded from 	|

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.1/lib/gitlab/ci/templates/references/certs/CertificateOfAuthoritySetup.yml
```

---

### Gradle Wrapper Configuration (job)

Enables caching in GitLab to reuse the gradle wrapper between jobs and gives the gradle wrapper executable file permissions.

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.1/lib/gitlab/ci/templates/references/gradle/GradleWrapperSetup.yml
```

---

### Gradle Test (job)

Runs tests through Gradle commands and publishes the results as an artifact to GitLab. These test result artifacts can be viewed by going to your project's CI pipelines page and then selecting the context menu on the right hand of the test job.

#### GitLab Artifacts
- Tests results found in the build/test-results/test/ directory. This is the default location for JUnit test results.

#### Customization

| Variable          	| Description                                            	|
|-------------------	|--------------------------------------------------------	|
| EXTRA_GRADLE_TEST_FLAGS 	| Flags that will be appended to the gradle test command 	|

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.1/lib/gitlab/ci/templates/jobs/gradle/Test.yml
```

---

### Publish Jar (job)
Publishes a SNAPSHOT jar whenever a feature branch is merged into the project's default branch and publishes release jars when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below). After performing a release build, the project's version is automatically updated and the change is committed to the repo. Javadocs are also published with releases.

#### Customization

| Variable                	| Default Value                                                        	| Description                                                                                                                                                                               	|
|-------------------------	|----------------------------------------------------------------------	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   |
| STANDARD_GRADLE_FLAGS   	|           | -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain  (-PsafeTest)	| Default Gradle flags that will be appended to all Gradle commands (Will include -PsafeTest when SAFE_TEST is set to "true"))                                                                                        |
| PUBLISH_SNAPSHOT_GRADLE_FLAGS  |                                                                    	| Gradle flags for customizing the snapshot & release publish tasks                                                                                                                             |
| RELEASE_GRADLE_FLAGS | -x updateReleaseVersion -x tagRelease | Flags passed to the gradle command used to publish release jars.
| GIT_TASKS_ENABLED         | true                                                                  | Determines whether any gradle tasks that perform Git operations with be included in the pipeline. If disabled a project's version will not be automatically updated following a release build |
| DEV_REGEX                 | develop                                                               | Branch(es) SNAPSHOT builds will be published from when new commits are made. For example, if it's desired to build SNAPSHOTs from `v2-develop` and `v3-develop` branches, this variable can be set to `'^v3-develop\|$^v2-develop$'`
| SAFE_TEST     | false     | Boolean on whether to run the build pipeline as a test before actually deploying, when set to \"true\" the build will not publish or deploy and artifacts.|
| TASK_ARGUMENTS    |       | Additional command line arguments and gradle tasks for this build. ex: \"-Pforce -x updateReleaseVersion\" These tasks will run on every job downstream.                                               |
| RELEASE                 	|                                                                      	| The name that will be appended to release build artifacts. By default a release candidate will be created from this unless the value "final" is used   	                                    |

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/jobs/gradle/PublishJar.yml
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

| Variable              	| Default Value                                                        	| Description                                                                                                       	|
|-----------------------	|----------------------------------------------------------------------	|-------------------------------------------------------------------------------------------------------------------	|
| STANDARD_GRADLE_FLAGS 	| -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	| Default Gradle flags that will be appended to all Gradle commands                                                 	|
| JIB_FLAGS             	| -DsendCredentialsOverHttp=true                                       	| Gradle flags used to customize the JIB task. The default value enables publishing docker images to insecure registries 	|
| PUBLISH_DOCKER        	|                                                                      	| Flag to manually publish a docker image from a GitLab pipeline on a non-default branch                           	|
| DOCKER_REPO_HOSTNAME      |                                                                       | URL to docker repository, i.e. `harbor.eng.ctic-dev.com`                                                              |       
| DOCKER_REPO_USERNAME      |                                                                       | Username for that repository                                                                                          |
| DOCKER_REPO_PASSWORD      |                                                                       | Password for that repository                                                                                          | 
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.1/lib/gitlab/ci/templates/jobs/docker/Jib.yml
```

---

### IMG Docker Image Publishing (job)
Uses the [IMG toolchain](https://github.com/genuinetools/img) to build and publish docker images from a dockerfile. IMG is used in place of the standard Docker toolchain to circumvent security restrictions within GitLab pipelines.

#### Customization

| Variable             	| Description                                                                                                                 	|
|----------------------	|-----------------------------------------------------------------------------------------------------------------------------	|
| DOCKER_DIRECTORY     	| Declares the directory where the dockerfile is located. If not specified then the project's root directory will be searched 	|
| DOCKER_REPO_USERNAME 	| Username credentials for authentication used for the Docker registry that the image will be published to                             	|
| DOCKER_REPO_PASSWORD 	| Password credentials for authentication used for the Docker registry that the image will be published to                             	|
| DOCKER_REPO_HOSTNAME 	| The docker registry host to authenticate with.                                                                              	|
| APP_NAME             	| The unique identify that will be used as the tag for the docker image being built                                           	|
| APP_VERSION          	| The version used to tag the docker image being built                                                                        	|

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/jobs/docker/Img.yml
```

---

### SonarQube Analysis (job)
Runs SonarQube gradle tasks to analyze a repo and publish generated reports to a SonarQube instance.

#### Customization

| Variable          	| Description                                                       	|
|-------------------	|-------------------------------------------------------------------	|
| SONAR_PROJECT_KEY 	| The unique identifier of the project generated in SonarQube       	|
| SONAR_HOST_URL    	| The base SonarQube URL where analysis results are published 	        |
| SONAR_LOGIN_TOKEN 	| An authentication token generated by SonarQube             	        |

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/jobs/gradle/SonarQube.yml
```

---

### Publish Helm Chart (jobs)
Runs a lint check to validate the integrity of the project's helm chart and subsequently publishes the helm chart to a registry 

#### Customization

| Variables                 	| Default Value               	| Description                                                                          	    |
|---------------------------	|-----------------------------	|------------------------------------------------------------------------------------------	|
| PUBLISH_HELM_CHARTS_IMAGE 	| chesapeaketechnology/devops 	| The docker image used to build and publish the helm chart                            	    |
| HELM_CHART                	|                             	| The file descriptor of the zip file containing the helm chart's contents             	    |
| HELM_CHART_DIR            	|                             	| The path of the directory containing the helm chart                                  	    |
| CHART_REPO_NAME           	|                             	| The name of the group that the helm chart will be added to                           	    |
| CHART_PROJECT_NAME        	| $HELM_CHART                 	| The name that the helm chart will appear under in the chart registry                 	    |
| CHART_REPO_URL            	|                             	| The base URL of the chart registry excluding the group and project specific identifiers 	|

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/jobs/helm/PublishHelmChart.yml
```

## Change log

#### [1.1.0] on 2021-11-7 : Updated docker `jib` job to take credentials as an argument if config file is not present

#### [1.0.0] on 2021-06-20 : Initial migration and publication of templates to a public repo for shared usage across GitLab instances
- Initial release mirroring the capabilities pulled from existing standardized pipelines used at CTI.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[Apache](http://www.apache.org/licenses/)
