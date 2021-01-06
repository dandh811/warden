_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.1
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[32m[+][0m URL: https://liferewarded.ibotta.com/ [35.224.31.30]
[32m[+][0m Effective URL: https://liferewarded.ibotta.com/welcome/
[32m[+][0m Started: Thu Jun  4 17:00:30 2020

Interesting Finding(s):

[32m[+][0m Headers
 | Interesting Entries:
 |  - Server: nginx
 |  - X-Powered-By: WP Engine
 |  - X-Cacheable: bot
 |  - X-Cache-Group: bot
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[32m[+][0m https://liferewarded.ibotta.com/robots.txt
 | Interesting Entries:
 |  - /wp-admin/
 |  - /wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m This site has 'Must Use Plugins': https://liferewarded.ibotta.com/wp-content/mu-plugins/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 80%
 | Reference: http://codex.wordpress.org/Must_Use_Plugins

[32m[+][0m The external WP-Cron seems to be enabled: https://liferewarded.ibotta.com/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[32m[+][0m WordPress version 5.4.1 identified (Latest, released on 2020-04-29).
 | Found By: Rss Generator (Passive Detection)
 |  - https://liferewarded.ibotta.com/feed/, <generator>https://wordpress.org/?v=5.4.1</generator>
 |  - https://liferewarded.ibotta.com/comments/feed/, <generator>https://wordpress.org/?v=5.4.1</generator>

[32m[+][0m WordPress theme in use: eyebottle
 | Location: https://liferewarded.ibotta.com/wp-content/themes/eyebottle/
 | Readme: https://liferewarded.ibotta.com/wp-content/themes/eyebottle/readme.txt
 | Style URL: https://liferewarded.ibotta.com/wp-content/themes/eyebottle/style.css?ver=5.4.1
 | Style Name: EyeBottle
 | Style URI: http://underscores.me/
 | Description: Description...
 | Author: Underscores.me
 | Author URI: http://underscores.me/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/themes/eyebottle/style.css?ver=5.4.1, Match: 'Version: 1.0.0'


[34m[i][0m Plugin(s) Identified:

[32m[+][0m addons-for-elementor
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/addons-for-elementor/
 | Latest Version: 2.9.9 (up to date)
 | Last Updated: 2020-04-05T04:01:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 2.9.9 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/addons-for-elementor/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/addons-for-elementor/readme.txt

[32m[+][0m elementor
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/elementor/
 | Last Updated: 2020-06-02T07:34:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 2.9.11
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 2.9.8 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=2.9.8
 |  - https://liferewarded.ibotta.com/wp-content/plugins/elementor/assets/js/frontend.min.js?ver=2.9.8
 | Confirmed By: Readme - Stable Tag (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/elementor/readme.txt

[32m[+][0m elementor-pro
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/elementor-pro/
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 2.9.4 (60% confidence)
 | Found By: Change Log (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/elementor-pro/changelog.txt, Match: '#### 2.9.4 -'

[32m[+][0m jet-tabs
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/jet-tabs/
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | The version could not be determined.

[32m[+][0m page-list
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/page-list/
 | Latest Version: 5.2 (up to date)
 | Last Updated: 2019-12-18T13:24:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 5.2 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/page-list/css/page-list.css?ver=5.2
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://liferewarded.ibotta.com/wp-content/plugins/page-list/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://liferewarded.ibotta.com/wp-content/plugins/page-list/readme.txt

[32m[+][0m premium-addons-for-elementor
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/premium-addons-for-elementor/
 | Last Updated: 2020-06-01T23:27:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 3.20.4
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 3.20.2 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/premium-addons-for-elementor/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/premium-addons-for-elementor/readme.txt

[32m[+][0m simple-embed-code
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/simple-embed-code/
 | Latest Version: 2.3.3 (up to date)
 | Last Updated: 2020-04-23T14:46:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 2.3.3 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/simple-embed-code/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/simple-embed-code/readme.txt

[32m[+][0m svg-support
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/svg-support/
 | Latest Version: 2.3.18 (up to date)
 | Last Updated: 2020-04-05T02:58:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 2.3.18 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/svg-support/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://liferewarded.ibotta.com/wp-content/plugins/svg-support/readme.txt

[32m[+][0m wordpress-seo
 | Location: https://liferewarded.ibotta.com/wp-content/plugins/wordpress-seo/
 | Last Updated: 2020-05-26T06:26:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 14.2
 |
 | Found By: Comment (Passive Detection)
 |
 | Version: 14.1 (100% confidence)
 | Found By: Comment (Passive Detection)
 |  - https://liferewarded.ibotta.com/welcome/, Match: 'optimized with the Yoast SEO plugin v14.1 -'
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://liferewarded.ibotta.com/wp-content/plugins/wordpress-seo/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://liferewarded.ibotta.com/wp-content/plugins/wordpress-seo/readme.txt


[34m[i][0m No Config Backups Found.

[32m[+][0m WPVulnDB API OK
 | Plan: free
 | Requests Done (during the scan): 11
 | Requests Remaining: 9

[32m[+][0m Finished: Thu Jun  4 17:01:13 2020
[32m[+][0m Requests Done: 95
[32m[+][0m Cached Requests: 4
[32m[+][0m Data Sent: 22.233 KB
[32m[+][0m Data Received: 777.116 KB
[32m[+][0m Memory used: 232.312 MB
[32m[+][0m Elapsed time: 00:00:42
