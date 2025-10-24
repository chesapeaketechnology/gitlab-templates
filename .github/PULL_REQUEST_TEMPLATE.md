### Checklist

- [ ] I have performed a self-review of my code.
- [ ] I have tested my changes against a Gitlab repo such as the CTI Getting Started Golden Path Templates.
- [ ] My changes generate no new warnings.
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have made corresponding changes to the documentation such as the README.md such as for new or changed variables.
- [ ] I have added notes to the CHANGELOG.md file.
- [ ] If I have edited a Gitlab job, I ensure the Gitlab job template can run independently of a Gitlab pipeline template. 
- [ ] I have ensured that if needed a downstream Gitlab job including my Gitlab job template can override the before_script and the Gitlab job template will still work. 
- [ ] My changes are not breaking changes, or if they are I have created a new release/<new-version>.x.x branch.
- [ ] If possible I have used images in the Gitlab jobs that are debian, not alpine, so commands like "apt-get" not "apkl" can be consistent across Gitlab jobs. 



