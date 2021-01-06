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

[32m[+][0m URL: https://sciencing.evonik.com/ [149.216.106.187]
[32m[+][0m Effective URL: https://sciencing.evonik.com/plf/
[32m[+][0m Started: Thu Jun  4 16:34:18 2020

Interesting Finding(s):

[32m[+][0m https://sciencing.evonik.com/plf/robots.txt
 | Interesting Entries:
 |  - /plf/wp-admin/
 |  - /plf/wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m XML-RPC seems to be enabled: https://sciencing.evonik.com/plf/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[32m[+][0m https://sciencing.evonik.com/plf/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m https://sciencing.evonik.com/plf/wp-content/debug.log
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | Reference: https://codex.wordpress.org/Debugging_in_WordPress

[32m[+][0m The external WP-Cron seems to be enabled: https://sciencing.evonik.com/plf/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[32m[+][0m WordPress version 5.3.1 identified (Insecure, released on 2019-12-12).
 | Found By: Rss Generator (Passive Detection)
 |  - https://sciencing.evonik.com/plf/feed/, <generator>https://wordpress.org/?v=5.3.1</generator>
 |  - https://sciencing.evonik.com/plf/comments/feed/, <generator>https://wordpress.org/?v=5.3.1</generator>
 |
 | [31m[!][0m 6 vulnerabilities identified:
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Password Reset Tokens Failed to Be Properly Invalidated
 |     Fixed in: 5.3.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10201
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11027
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47634/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-ww7v-jg8c-q6jw
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Unauthenticated Users View Private Posts
 |     Fixed in: 5.3.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10202
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11028
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47635/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-xhx9-759f-6p2w
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Authenticated Cross-Site Scripting (XSS) in Customizer
 |     Fixed in: 5.3.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10203
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11025
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47633/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-4mhg-j6fx-5g3c
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Authenticated Cross-Site Scripting (XSS) in Search Block
 |     Fixed in: 5.3.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10204
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11030
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47636/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-vccm-6gmc-qhjh
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Cross-Site Scripting (XSS) in wp-object-cache
 |     Fixed in: 5.3.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10205
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11029
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47637/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-568w-8m88-8g2c
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Authenticated Cross-Site Scripting (XSS) in File Uploads
 |     Fixed in: 5.3.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10206
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11026
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47638/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-3gw2-4656-pfr2

[32m[+][0m WordPress theme in use: betheme-child
 | Location: https://sciencing.evonik.com/plf/wp-content/themes/betheme-child/
 | Style URL: https://sciencing.evonik.com/plf/wp-content/themes/betheme-child/style.css?ver=21.3.1.1
 | Style Name: Betheme Child
 | Style URI: https://themes.muffingroup.com/betheme
 | Description: Child Theme for Betheme...
 | Author: Muffin group
 | Author URI: https://muffingroup.com
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.6.2 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://sciencing.evonik.com/plf/wp-content/themes/betheme-child/style.css?ver=21.3.1.1, Match: 'Version: 1.6.2'


[34m[i][0m Plugin(s) Identified:

[32m[+][0m cf7-countries
 | Location: https://sciencing.evonik.com/plf/wp-content/plugins/cf7-countries/
 | Latest Version: 1.0.0 (up to date)
 | Last Updated: 2019-02-24T15:45:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.0.0 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - https://sciencing.evonik.com/plf/wp-content/plugins/cf7-countries/public/css/cf7-countries-public.css?ver=1.0.0
 |  - https://sciencing.evonik.com/plf/wp-content/plugins/cf7-countries/public/js/cf7-countries-public.js?ver=1.0.0
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://sciencing.evonik.com/plf/wp-content/plugins/cf7-countries/README.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://sciencing.evonik.com/plf/wp-content/plugins/cf7-countries/README.txt

[32m[+][0m contact-form-7
 | Location: https://sciencing.evonik.com/plf/wp-content/plugins/contact-form-7/
 | Last Updated: 2020-05-20T05:30:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 5.1.9
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Hidden Input (Passive Detection)
 |
 | Version: 5.1.6 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - https://sciencing.evonik.com/plf/wp-content/plugins/contact-form-7/includes/css/styles.css?ver=5.1.6
 |  - https://sciencing.evonik.com/plf/wp-content/plugins/contact-form-7/includes/js/scripts.js?ver=5.1.6
 | Confirmed By:
 |  Hidden Input (Passive Detection)
 |   - https://sciencing.evonik.com/plf/, Match: '5.1.6'
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://sciencing.evonik.com/plf/wp-content/plugins/contact-form-7/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://sciencing.evonik.com/plf/wp-content/plugins/contact-form-7/readme.txt

[32m[+][0m itonics-simple_js_and_css_include
 | Location: https://sciencing.evonik.com/plf/wp-content/plugins/itonics-simple_js_and_css_include/
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | The version could not be determined.

[32m[+][0m mfn-header-builder
 | Location: https://sciencing.evonik.com/plf/wp-content/plugins/mfn-header-builder/
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | The version could not be determined.

[32m[+][0m sitepress-multilingual-cms
 | Location: https://sciencing.evonik.com/plf/wp-content/plugins/sitepress-multilingual-cms/
 | Latest Version: 2.0.4.1 (up to date)
 | Last Updated: 2011-06-05T13:40:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Meta Generator (Passive Detection)
 |
 | [31m[!][0m 1 vulnerability identified:
 |
 | [31m[!][0m Title: WPML < 4.3.7 - Authenticated Cross Site Request Forgery leading to Remote Code Execution
 |     Fixed in: 4.3.7
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10131
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-10568
 |      - https://medium.com/@arall/sitepress-multilingual-cms-wplugin-wpml-4-3-7-b-2-9c9486c13577
 |
 | Version: 4.3.5 (70% confidence)
 | Found By: Dependencies File (Aggressive Detection)
 |  - https://sciencing.evonik.com/plf/wp-content/plugins/sitepress-multilingual-cms/wpml-dependencies.json, Match: '4.3.5'

[32m[+][0m smart-slider-3
 | Location: https://sciencing.evonik.com/plf/wp-content/plugins/smart-slider-3/
 | Last Updated: 2020-05-21T11:58:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 3.4.1.7
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 3.3.25 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://sciencing.evonik.com/plf/wp-content/plugins/smart-slider-3/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://sciencing.evonik.com/plf/wp-content/plugins/smart-slider-3/readme.txt

[32m[+][0m wordpress-seo
 | Location: https://sciencing.evonik.com/plf/wp-content/plugins/wordpress-seo/
 | Last Updated: 2020-05-26T06:26:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 14.2
 |
 | Found By: Comment (Passive Detection)
 |
 | Version: 13.1 (100% confidence)
 | Found By: Comment (Passive Detection)
 |  - https://sciencing.evonik.com/plf/, Match: 'optimized with the Yoast SEO plugin v13.1 -'
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://sciencing.evonik.com/plf/wp-content/plugins/wordpress-seo/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://sciencing.evonik.com/plf/wp-content/plugins/wordpress-seo/readme.txt


[34m[i][0m No Config Backups Found.

[32m[+][0m WPVulnDB API OK
 | Plan: free
 | Requests Done (during the scan): 9
 | Requests Remaining: 26

[32m[+][0m Finished: Thu Jun  4 16:36:48 2020
[32m[+][0m Requests Done: 95
[32m[+][0m Cached Requests: 3
[32m[+][0m Data Sent: 35.299 KB
[32m[+][0m Data Received: 496.001 KB
[32m[+][0m Memory used: 226.125 MB
[32m[+][0m Elapsed time: 00:02:29
