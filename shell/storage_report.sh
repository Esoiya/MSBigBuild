#!/bin/bash

# Tool run by cron daily to generate and send reports by email and logging to the $log_path
# Email addresses should be stored at the $email_path in a file named $email_list


date_str=$(date +"%Y_%m_%d")

log_path=/var/log/report
filename=${date_str}_storage_report.txt
log_file=${log_path}/${date_str}_storage_report.log
email_path=/etc/reporting
email_list=${email_path}/emails

message_subject="Storage report ${date_str}"
message_body="Storage report summary is attached."

if [ ! -d "$log_path" ]
then
    mkdir -p $log_path
fi

if [ ! -d "$email_path" ]
then
    mkdir -p $email_path
fi

df -h > $filename

echo '' >> $filename
echo '######################################################################' >> $filename
echo '' >> $filename

repquota -a >> $filename

echo '' > $log_file
if [ -f "$email_list" ]
then
	email_adresses=$(cat ${email_list})
	for email in $email_adresses
	do
		mail -s "$message_subject" -a $filename $email <<< "$message_body"
		echo "Email sent to: ${email}" >> $log_file
	done
else
	echo "Email file missing!" >> $log_file
fi

echo '' >> $log_file
echo 'Content:' >> $log_file
cat $filename >> $log_file

rm -f $filename