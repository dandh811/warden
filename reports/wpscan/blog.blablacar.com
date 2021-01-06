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

[32m[+][0m URL: https://blog.blablacar.com/ [35.197.217.214]
[32m[+][0m Started: Thu Jun  4 17:06:05 2020

Interesting Finding(s):

[32m[+][0m Headers
 | Interesting Entries:
 |  - Server: nginx
 |  - X-Powered-By: WP Engine
 |  - X-Cacheable: bot
 |  - X-Cache-Group: bot
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[32m[+][0m https://blog.blablacar.com/robots.txt
 | Interesting Entries:
 |  - /wp-admin/
 |  - /wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m XML-RPC seems to be enabled: https://blog.blablacar.com/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[32m[+][0m This site has 'Must Use Plugins': https://blog.blablacar.com/wp-content/mu-plugins/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 80%
 | Reference: http://codex.wordpress.org/Must_Use_Plugins

[32m[+][0m The external WP-Cron seems to be enabled: https://blog.blablacar.com/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[32m[+][0m WordPress version 5.4.1 identified (Latest, released on 2020-04-29).
 | Found By: Most Common Wp Includes Query Parameter In Homepage (Passive Detection)
 |  - https://blog.blablacar.com/wp-includes/css/dist/block-library/style.min.css?ver=5.4.1
 | Confirmed By: Style Etag (Aggressive Detection)
 |  - https://blog.blablacar.com/wp-admin/load-styles.php, Match: '5.4.1'

[32m[+][0m WordPress theme in use: wp-blablalife
 | Location: https://blog.blablacar.com/wp-content/themes/wp-blablalife/
 | Readme: https://blog.blablacar.com/wp-content/themes/wp-blablalife/README.md
 | Style URL: https://blog.blablacar.com/wp-content/themes/wp-blablalife/style.css
 | Style Name: Blablalife Theme
 | Style URI: https://github.com/blablacar/wp-blablalife
 | Author: Chilid
 | Author URI: https://chilidagency.com/
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.7.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://blog.blablacar.com/wp-content/themes/wp-blablalife/style.css, Match: 'Version:            1.7.5'


[34m[i][0m Plugin(s) Identified:

[32m[+][0m instagram-feed
 | Location: https://blog.blablacar.com/wp-content/plugins/instagram-feed/
 | Latest Version: 2.4.3 (up to date)
 | Last Updated: 2020-05-28T18:07:00.000Z
 |
 | Found By: Javascript Var (Passive Detection)
 |
 | Version: 2.4.3 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://blog.blablacar.com/wp-content/plugins/instagram-feed/README.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://blog.blablacar.com/wp-content/plugins/instagram-feed/README.txt

[32m[+][0m wordpress-23-related-posts-plugin
 | Location: https://blog.blablacar.com/wp-content/plugins/wordpress-23-related-posts-plugin/
 | Latest Version: 3.6.4 (up to date)
 | Last Updated: 2018-05-25T11:00:00.000Z
 |
 | Found By: Javascript Var (Passive Detection)
 |
 | Version: 3.6.4 (100% confidence)
 | Found By: Javascript Var (Passive Detection)
 |  - https://blog.blablacar.com/, Match: 'window._wp_rp_plugin_version = '3.6.4';'
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://blog.blablacar.com/wp-content/plugins/wordpress-23-related-posts-plugin/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://blog.blablacar.com/wp-content/plugins/wordpress-23-related-posts-plugin/readme.txt

[32m[+][0m wordpress-seo
 | Location: https://blog.blablacar.com/wp-content/plugins/wordpress-seo/
 | Latest Version: 14.2 (up to date)
 | Last Updated: 2020-05-26T06:26:00.000Z
 |
 | Found By: Comment (Passive Detection)
 |
 | Version: 14.2 (100% confidence)
 | Found By: Comment (Passive Detection)
 |  - https://blog.blablacar.com/, Match: 'optimized with the Yoast SEO plugin v14.2 -'
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://blog.blablacar.com/wp-content/plugins/wordpress-seo/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://blog.blablacar.com/wp-content/plugins/wordpress-seo/readme.txt


[34m[i][0m No Config Backups Found.

[32m[+][0m WPVulnDB API OK
 | Plan: free
 | Requests Done (during the scan): 5
 | Requests Remaining: 0

[32m[+][0m Finished: Thu Jun  4 17:07:15 2020
[32m[+][0m Requests Done: 74
[32m[+][0m Cached Requests: 18
[32m[+][0m Data Sent: 15.147 KB
[32m[+][0m Data Received: 543.948 KB
[32m[+][0m Memory used: 207.43 MB
[32m[+][0m Elapsed time: 00:01:10
