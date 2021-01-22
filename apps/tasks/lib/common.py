payload = " AND 1=1 UNION ALL SELECT 1,NULL,'<script>alert(XSS)</script>',table_name FROM information_schema.tables WHERE 2>1--/**/; EXEC xp_cmdshell('cat ../../../etc/passwd')"


def update_scan_status(target, type):
    try:
        cur_scan_status = target.scanned
        if cur_scan_status == 'not':
            target.scanned = type
        elif type not in cur_scan_status:
            target.scanned = cur_scan_status + ',' + type
        target.save()
    except Exception as e:
        pass
