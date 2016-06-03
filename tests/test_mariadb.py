from subprocess import check_call
import time
import docker
import pytest


@pytest.fixture(scope='module')
def cli(request):
    return docker.Client()


@pytest.fixture(scope='module')
def container(cli):
    return cli.containers(
        filters={"label": "com.docker.compose.service=mariadb"})[0]


def setup_module(module):
    check_call(['docker-compose', 'up', '-d'])
    time.sleep(30)


def teardown_module(module):
    check_call(['docker-compose', 'down'])


def test_mysql_check_mysqld(cli, container):
    res = cli.exec_create(container['Id'], "pgrep mysql")
    cli.exec_start(res)
    assert cli.exec_inspect(res)['ExitCode'] == 0


def test_mysql_is_running():
    cmd = ['nc', '-z', '-v', '-w5', '127.0.0.1', '33306']
    check_call(cmd)


def test_mysql_is_accessible(cli, container):
    cmd = ("bash -c 'mysql -Ns -h127.0.0.1 -uroot -p$DB_ROOT_PASSWORD"
           " -e \"SHOW DATABASES\"'")
    res = cli.exec_create(container['Id'], cmd)
    out = cli.exec_start(res)
    assert cli.exec_inspect(res)['ExitCode'] == 0
    out = filter(bool, out.split('\n'))
    assert set(out) == \
        set(['information_schema', 'mysql', 'performance_schema'])
