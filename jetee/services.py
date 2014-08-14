from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.runtime.configuration import project_configuration

__all__ = [u'AppService', u'PostgreSQLService', u'RedisService']


class AppService(DockerServiceAbstract):
    image = u'whackojacko/blank'
    command = u'supervisord --nodaemon'
    volumes = [u'/root/.ssh/:/root/.ssh']
    ports_mappings = [
        PortsMapping(internal_port=22, interface=u'0.0.0.0'),  #for sshd
        PortsMapping(internal_port=9000, interface=u'172.17.42.1')  #for project itself
    ]

    @property
    def container_name(self):
        return u'project'

    @property
    def container_full_name(self):
        return u'.'.join([project_configuration.project_name, u'project'])


class PostgreSQLService(DockerServiceAbstract):
    image = u'zumbrunnen/postgresql'
    command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=5432
        )
    ]


class RedisService(DockerServiceAbstract):
    image = u'redis'
    command = u'redis-server'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=6379
        )
    ]