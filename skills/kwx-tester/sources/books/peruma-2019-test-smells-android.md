# On the Distribution of Test Smells in Open Source Android Applications: An Exploratory Study

- Authors: Anthony Peruma, Khalid Almalki, Christian D. Newman, Mohamed Wiem Mkaouer, Ali Ouni, Fabio Palomba
- Year: 2019 (CASCON 2019)
- Legal URL: https://www.rit.edu/academicaffairs/facultyscholarship/submit/download_file.php?id=66568 (RIT faculty scholarship repository); tool and smell definitions at https://testsmells.org

## What I read

The smell definitions (section 2), the developer survey (49 responses), the data collection (656 apps with tests, 1,187,055 test methods), Table 3 (share of apps and files per smell) and the co-occurrence discussion. Also the tsDetect smell list on testsmells.org (19 smells with detection rules).

## Key lessons used in quality/test-smells.md

- 97% of apps with tests had test smells; a test file had 3 smell types on average.
- Share of test files per smell: Assertion Roulette 58.5%, Exception Handling 49.2%, Eager Test 38.7%, Magic Number 34.8%, Unknown Test 34.4%, Duplicate Assert 31.3%, Lazy Test 29.5%, Conditional Test Logic 28.7%, Mystery Guest 11.7%, Sleepy Test 2.0%, Empty Test 1.1%.
- Developers agreed unanimously that empty tests and print statements should go; were split on ignored tests and conditional logic; said magic numbers need a constant only when the number has a hidden meaning.
- Sleepy tests are used for animations and load times; developers know they are risky but see no easy alternative.
- tsDetect reports precision 85 to 100% and recall 90 to 100% on its own benchmark (Java only), so the skill uses its definitions but its own scanner for JS, Rust, Kotlin and Python.
