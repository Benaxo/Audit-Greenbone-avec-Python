import time
from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp

def authenticate_gmp():
    connection = TLSConnection(hostname='127.0.0.1', port=9390)
    gmp = Gmp(connection)
    username = 'admin'
    password = 'password'

    gmp.authenticate(username, password)
    return gmp

def run_scan(gmp, target_ip):
    target_name = "Target"
    response = gmp.create_target(name=target_name, hosts=[target_ip])
    target_id = response.xpath('//@id')[0]

    scan_name = "Scan"
    config_id = "daba56c8-73ec-11df-a475-002264764cea"  # Full and fast
    response = gmp.create_task(name=scan_name, config_id=config_id, target_id=target_id)
    task_id = response.xpath('//@id')[0]

    gmp.start_task(task_id)
    while True:
        time.sleep(30)
        task_status = gmp.get_task(task_id=task_id).xpath('//status/text()')[0]
        if task_status == "Done":
            break

    report_id = gmp.get_task(task_id=task_id).xpath('//last_report/report/@id')[0]
    report_format_id = gmp.get_report_formats()[0].xpath('//report_format[name="Anonymous XML"]/@id')[0]
    response = gmp.get_report(report_id=report_id, report_format_id=report_format_id)
    report = response.xpath('//report/text()')[0]

    return report

def main():
    gmp = authenticate_gmp()
    target_ip = "192.168.17.142"
    report = run_scan(gmp, target_ip)

    with open("openvas_report.json", "w") as file:
        file.write(report)

if __name__ == "__main__":
    main()
