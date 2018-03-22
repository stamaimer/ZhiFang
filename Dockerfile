FROM python:2
COPY . /ZhiFang
WORKDIR /ZhiFang
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com
CMD ["/bin/sh", "start_script.sh"]

