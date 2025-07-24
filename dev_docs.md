# Developer Documentations



### File Structure:

1. <b>`services/`</b> Thread Safe Services

    * `metrics.py` Continous Glucose Monitoring metrics service that is responsible for calculating CGM metrics like rate of change and missing reading alerts.
    * `Status.py` Status service, read from `status.json`.
    * `Telegram.py` Telegram Bot service functionality.

2. <b>`localization/`</b> Localization JSON files supporting 33 langueages and dielects.

3. **`utils/`**

    * `Localize.py` localization functionality built on JSON files in `localization/`.

    * `PrintLog.py` overwrite builtin **print()** to do logging instead of printing to console. also has **error()** for errors in logs and **panic()** which logs errors then terminate the program.

    * `Settings.py` loads **configs.json** into a global variables for settings.

    * `SlidingWindow.py` a sliding window for moving averages and plotting

4. **`tools/`** utilities used for deployment and maintainance

    * `deamon.py` CLI too to creates a SystemD deamon for python projects.



### Conventions and terminology:

> ###### TS: Thread Safe class or library


