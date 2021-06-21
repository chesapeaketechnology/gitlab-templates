# GitLab Pipeline Templates

GitLab Pipeline Templates is a collection of shared GitLab jobs and pipelines aimed at simplifying the process of setting up and maintaining the continuous integration tasks. These templates include tasks to run build scripts, unit tests, and to publish artifacts.

## Usage
### Versioning
It's important to understand that these templates are versioned by branches in GitLab to improve stability between changes. Release branches will only make additive changes and backwards compatible changes. The master branch will always be updated with the latest changes which can cause your pipelines to break. For this reason it is **not** recommended to depend directly on the master branch when using these templates.

### Getting Started
Inside the root directory of your project, create a file named `.gitlab-ci.yml` and copy the content from the section(s) below that most closely match your needs. Multiple include statements can be combined to capture all of the jobs that you want to capture in your pipeline. 

### Standard Gradle Pipeline
The standard gradle pipeline is the simplest way to get up an running quickly. It provides a full pipeline configuration that will build, test, and publish jars from a project. By default, SNAPSHOTS are published whenever a branch is merged into the "default" branch. Release jars are only created when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below) from a branch following the naming convention `feature/{version}`. 

#### Linked Jobs
- [Certificate of Authority Configuration](#certificate-of-authority-configuration-job)
- [Gradle Wrapper Configuration](#gradle-wrapper-configuration-job)
- [Test](#gradle-test-job)
- [Publish Jar](#publish-jar-job)

#### Customization
| Variable                	| Default Value                                                        	| Description                                                                                                                                            	|
|-------------------------	|----------------------------------------------------------------------	|--------------------------------------------------------------------------------------------------------------------------------------------------------	|
| DEFAULT IMAGE           	| openjdk:8                                                            	| The base docker image used to run all included jobs. Jobs can also be further customized by specifying a different image for a specific job.           	|
| STANDARD_GRADLE_FLAGS   	| -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	| Default Gradle flags that will be appended to all Gradle commands                                                                                         |
| EXTRA_GRADLE_TEST_FLAGS 	|                                                                      	| Flags that will appended to test tasks.                                                                                                                	|
| RELEASE                 	|                                                                      	| The name that will be appended to release build artifacts. By default an release candidate will be created from this unless the value "final" is used. 	|

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/pipeline/GradleJavaPipeline.yml
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
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/references/certs/CertificateOfAuthoritySetup.yml
```

---

### Gradle Wrapper Configuration (job)

Enables caching in GitLab to reuse the gradle wrapper between jobs and gives the gradle wrapper executable file permissions.

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/references/gradle/GradleWrapperSetup.yml
```

---

### Gradle Test (job)

Runs tests through Gradle commands and publishes the results as an artifact to GitLab. These test result artifacts can be viewed by going to your project's CI pipelines page and then selecting the context menu on the right hand of the test job.

#### GitLab Artifacts
- Tests results found in the build/test-results/test/ directory. This is the default location for JUnit test results.

#### Customization

| Variable          	| Description                                            	|
|-------------------	|--------------------------------------------------------	|
| GRADLE_TEST_FLAGS 	| Flags that will be appended to the gradle test command 	|

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/jobs/gradle/Test.yml
```

---

### Publish Jar (job)
Publishes build artifacts from the repository. SNAPSHOTS are published whenever a branch is merged into a "protected" branch; by default the "master" branch is the only protected branch within a repo, but you can declare other protected branches such as "develop" from GitLab's project configurations. Release jars are only created when a GitLab pipeline is manually triggered with the "RELEASE" environment variable defined (values described below).

#### Customization

| Variable                	| Default Value                                                        	| Description                                                                                                                                            	|
|-------------------------	|----------------------------------------------------------------------	|--------------------------------------------------------------------------------------------------------------------------------------------------------	|
| STANDARD_GRADLE_FLAGS   	| -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	| Default Gradle flags that will be appended to all Gradle commands                                                                                         |
| RELEASE                 	|                                                                      	| The name that will be appended to release build artifacts. By default a release candidate will be created from this unless the value "final" is used. 	|

#### Reference URL
```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/jobs/gradle/PublishJar.yml
```

---

### JIB Docker Image Publishing(job)
Uses the gradle [JIB Gradle plugin](https://github.com/GoogleContainerTools/jib/tree/master/jib-gradle-plugin) to build and publish docker images. 

#### Customization

| Variable              	| Default Value                                                        	| Description                                                                                                       	|
|-----------------------	|----------------------------------------------------------------------	|-------------------------------------------------------------------------------------------------------------------	|
| STANDARD_GRADLE_FLAGS 	| -s --no-daemon -PnoMavenLocal --refresh-dependencies --console=plain 	| Default Gradle flags that will be appended to all Gradle commands                                                 	|
| JIB_FLAGS             	| -DsendCredentialsOverHttp=true                                       	| Gradle flags used to customize the JIB task. The default value enables publishing docker images to insecure registries 	|
| PUBLISH_DOCKER        	|                                                                      	| Flag to manually publish a docker image from a GitLab pipeline on a non-default branch                           	|

```
include:
  - remote: https://raw.githubusercontent.com/chesapeaketechnology/gitlab-templates/release/1.0/lib/gitlab/ci/templates/jobs/docker/Jib.yml
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

#### [1.0.0] on 2021-06-20 : Initial migration and publication of templates to a public repo for shared usage across GitLab instances
- Initial release mirroring the capabilities pulled from existing standardized pipelines used at CTI.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[Apache](http://www.apache.org/licenses/)