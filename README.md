# testcase to reproduce "flapping" in asottile/seed-isort-config

This test case reproduces a bug in [seed-isort-config][].

The conditions for the bug are the following:

1. There is more than one third-party module used in the Python source files
    visited by [seed-isort-config][].
2. There is exactly one of those third-party modules listed in the value for
    the `known_third_party` key in [.isort.cfg][].
3. A `known_first_party` key exists in [.isort.cfg][] with no value.


 [seed-isort-config]: https://github.com/asottile/seed-isort-config
 [forked seed-isort-config]: https://github.com/jmknoble/seed-isort-config
 [.isort.cfg]: .isort.cfg


## How to Reproduce

> :pushpin: ***NOTE:***
>
> When checking out tags in the steps below, you will likely end up in
> "detached HEAD" state; that is normal and to be expected, and it will not
> affect the steps below (in fact, the steps depend on it).

1. Clone [this repository](https://github.com/jmknoble/testcase-seed-isort-config).
2. Check out the `before-seeding` tag and verify behavior with an empty
    `known_third_party` key.
3. Check out the `seeded-with-1-third-party-module` tag and verify behavior
    with a single module in the source and single module in the
    `known_third_party` key.
4. Check out the `with-2-third-party-modules` tag and verify the behavior with
    one module in the `known_third_party` key and two modules in the source.
5. Check out the `without-greedy-whitespace` and verify the fix works without
    greedy whitespace.

Transcripts and expected behaviors below.

### 1. Clone this repository

If you're reading this, this step should either be self-explanatory or have
already occurred.


### 2. before-seeding

Expected behavior:

- **seed-isort-config** adds the third-party module to the `known_third_party`
    key the first time it runs, failing the pre-commit hook.
- Subsequent runs do not further modify **.isort.cfg**, allowing the
    pre-commit hook to pass.

Actual behavior:

- As expected.

```diff
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [master|✔]
11:57 $ git checkout before-seeding
Note: checking out 'before-seeding'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at 3da4798 Make test case as minimal as possible
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✔]
11:57 $ cat .pre-commit-config.yaml
---
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks

default_language_version:
  python: python3

repos:
  - repo: https://github.com/asottile/seed-isort-config
    rev: v1.9.1
    hooks:
      - id: seed-isort-config
        args: ['--exclude=(docs?|examples?|tests?|utils?)/.*\.py']
...
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✔]
11:57 $ cat .isort.cfg
# https://github.com/timothycrosley/isort

[settings]

known_first_party =

known_third_party =
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✔]
11:57 $ cat testcase.py
#!/usr/bin/env python

import os
import sys

import dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✔]
11:57 $ pre-commit run --all-files
seed isort known_third_party.............................................Failed
hookid: seed-isort-config

Files were modified by this hook.

✘-1 ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✚ 1]
11:58 $ git diff
diff --git a/.isort.cfg b/.isort.cfg
index ca68bd8..cf6a930 100644
--- a/.isort.cfg
+++ b/.isort.cfg
@@ -4,4 +4,4 @@

 known_first_party =

-known_third_party =
+known_third_party =dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✚ 1]
11:58 $ pre-commit run --all-files
seed isort known_third_party.............................................Passed
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✚ 1]
11:58 $ git diff
diff --git a/.isort.cfg b/.isort.cfg
index ca68bd8..cf6a930 100644
--- a/.isort.cfg
+++ b/.isort.cfg
@@ -4,4 +4,4 @@

 known_first_party =

-known_third_party =
+known_third_party =dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✚ 1]
11:58 $
```


### 3. seeded-with-1-third-party-module

Expected behavior:

- **seed-isort-config** does not further modify **.isort.cfg**, allowing the
    pre-commit hook to pass.

Actual behavior:

- As expected.

```diff
✘-1 ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [before-seeding|✚ 1]
11:59 $ git checkout -f seeded-with-1-third-party-module
Previous HEAD position was 3da4798 Make test case as minimal as possible
HEAD is now at 4231648 Effects of running seed-isort-config with one 3rd-party module
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [seeded-with-1-third-party-module|✔]
11:59 $ cat .isort.cfg
# https://github.com/timothycrosley/isort

[settings]

known_first_party =

known_third_party =dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [seeded-with-1-third-party-module|✔]
11:59 $ cat testcase.py
#!/usr/bin/env python

import os
import sys

import dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [seeded-with-1-third-party-module|✔]
12:00 $ pre-commit run --all-files
seed isort known_third_party.............................................Passed
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [seeded-with-1-third-party-module|✔]
12:00 $ cat .isort.cfg
# https://github.com/timothycrosley/isort

[settings]

known_first_party =

known_third_party =dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [seeded-with-1-third-party-module|✔]
12:00 $ pre-commit run --all-files
seed isort known_third_party.............................................Passed
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [seeded-with-1-third-party-module|✔]
12:00 $
```


### 4. with-2-third-party-modules

Expected behavior:

- **seed-isort-config** adds the 2nd third-party module to the
    `known_third_party` key the first time it runs, failing the pre-commit hook.
- Subsequent runs do not further modify **.isort.cfg**, allowing the
    pre-commit hook to pass.

Actual behavior:

- **seed-isort-config** adds the 2nd third-party module to the
    `known_third_party` key the first time it runs, as expected.
- The second run, **seed-isort-config** unexpectedly _removes_ the 2nd
    third-party module, failing the pre-commit hook.
- The third run, **seed-isort-config** again adds the 2nd third-party module.
- An endless loop of failed pre-commit hooks results.

```diff
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [seeded-with-1-third-party-module|✔]
12:00 $ git checkout -f with-2-third-party-modules
Previous HEAD position was 4231648 Effects of running seed-isort-config with one 3rd-party module
HEAD is now at fad3a6c Add second third-party module
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✔]
12:01 $ cat .isort.cfg
# https://github.com/timothycrosley/isort

[settings]

known_first_party =

known_third_party =dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✔]
12:01 $ cat testcase.py
#!/usr/bin/env python

import os
import sys

import dummy_thirdparty1
import dummy_thirdparty2
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✔]
12:01 $ pre-commit run --all-files
seed isort known_third_party.............................................Failed
hookid: seed-isort-config

Files were modified by this hook.

✘-1 ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✚ 1]
12:01 $ git diff
diff --git a/.isort.cfg b/.isort.cfg
index cf6a930..0cf7afe 100644
--- a/.isort.cfg
+++ b/.isort.cfg
@@ -4,4 +4,4 @@

 known_first_party =

-known_third_party =dummy_thirdparty1
+known_third_party =dummy_thirdparty1,dummy_thirdparty2
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✚ 1]
12:01 $ pre-commit run --all-files
seed isort known_third_party.............................................Failed
hookid: seed-isort-config

Files were modified by this hook.

✘-1 ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✔]
12:01 $ git diff
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✔]
12:01 $ cat .isort.cfg
# https://github.com/timothycrosley/isort

[settings]

known_first_party =

known_third_party =dummy_thirdparty1
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✔]
12:01 $ pre-commit run --all-files
seed isort known_third_party.............................................Failed
hookid: seed-isort-config

Files were modified by this hook.

✘-1 ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✚ 1]
12:01 $ git diff
diff --git a/.isort.cfg b/.isort.cfg
index cf6a930..0cf7afe 100644
--- a/.isort.cfg
+++ b/.isort.cfg
@@ -4,4 +4,4 @@

 known_first_party =

-known_third_party =dummy_thirdparty1
+known_third_party =dummy_thirdparty1,dummy_thirdparty2
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [with-2-third-party-modules|✚ 1]
12:02 $
```


### 5. without-greedy-whitespace

Expected behavior:

- The [forked seed-isort-config][] adds the 2nd third-party module to the `known_third_party` key the first time it runs, failing the pre-commit hook.
- Subsequent runs do not further modify **.isort.cfg**, allowing the
  pre-commit hook to pass.

Actual behavior:

- As expected.

```diff
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✔]
12:07 $ git checkout -f without-greedy-whitespace
HEAD is now at c18169d Use forked seed-isort-config without greedy whitespace in regex
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✔]
12:07 $ git diff with-2-third-party-modules
diff --git a/.pre-commit-config.yaml b/.pre-commit-config.yaml
index d99ef69..16a5e3d 100644
--- a/.pre-commit-config.yaml
+++ b/.pre-commit-config.yaml
@@ -6,8 +6,8 @@ default_language_version:
   python: python3

 repos:
-  - repo: https://github.com/asottile/seed-isort-config
-    rev: v1.9.1
+  - repo: https://github.com/jmknoble/seed-isort-config
+    rev: v1.9.2
     hooks:
       - id: seed-isort-config
         args: ['--exclude=(docs?|examples?|tests?|utils?)/.*\.py']
diff --git a/VERSION b/VERSION
index 0d91a54..1d0ba9e 100644
--- a/VERSION
+++ b/VERSION
@@ -1 +1 @@
-0.3.0
+0.4.0
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✔]
12:07 $ pre-commit run --all-files
seed isort known_third_party.............................................Failed
hookid: seed-isort-config

Files were modified by this hook.

✘-1 ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✚ 1]
12:07 $ git diff
diff --git a/.isort.cfg b/.isort.cfg
index cf6a930..0cf7afe 100644
--- a/.isort.cfg
+++ b/.isort.cfg
@@ -4,4 +4,4 @@

 known_first_party =

-known_third_party =dummy_thirdparty1
+known_third_party =dummy_thirdparty1,dummy_thirdparty2
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✚ 1]
12:07 $ pre-commit run --all-files
seed isort known_third_party.............................................Passed
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✚ 1]
12:08 $ git diff
diff --git a/.isort.cfg b/.isort.cfg
index cf6a930..0cf7afe 100644
--- a/.isort.cfg
+++ b/.isort.cfg
@@ -4,4 +4,4 @@

 known_first_party =

-known_third_party =dummy_thirdparty1
+known_third_party =dummy_thirdparty1,dummy_thirdparty2
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✚ 1]
12:08 $ pre-commit run --all-files
seed isort known_third_party.............................................Passed
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✚ 1]
12:08 $ pre-commit run --all-files
seed isort known_third_party.............................................Passed
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✚ 1]
12:08 $ git diff
diff --git a/.isort.cfg b/.isort.cfg
index cf6a930..0cf7afe 100644
--- a/.isort.cfg
+++ b/.isort.cfg
@@ -4,4 +4,4 @@

 known_first_party =

-known_third_party =dummy_thirdparty1
+known_third_party =dummy_thirdparty1,dummy_thirdparty2
✔ ~/Stuff/RevisionControl/github.com/jmknoble/testcase-seed-isort-config [without-greedy-whitespace|✚ 1]
12:08 $
```
