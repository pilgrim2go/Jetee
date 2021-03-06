from jetee.base.deployment_manager import AbstractDeploymentManager
from jetee.common.config_factories.os.docker import DockerPackageAnsibleConfigFactory, \
    DockerPyPackageAnsibleConfigFactory
from jetee.common.config_factories.os.apt import UpdateAptCachePackageAnsibleConfigFactory
from jetee.common.config_factories.os.python import PythonDependenciesAnsibleConfigFactory
from jetee.service.services.docker_hosts import DockerHostsService
from jetee.common.config_factories.os.nginx import NginxPackageBootstrapAnsibleRoleConfigFactory
from jetee.common.config_factories.service.hosts import HostsFileExistsAnsiblePreTaskConfigFactory


class DockerServiceDeploymentManager(AbstractDeploymentManager):
    default_config_factories = (
        UpdateAptCachePackageAnsibleConfigFactory,
        DockerPackageAnsibleConfigFactory,
        PythonDependenciesAnsibleConfigFactory,
        DockerPyPackageAnsibleConfigFactory,
        NginxPackageBootstrapAnsibleRoleConfigFactory,
        HostsFileExistsAnsiblePreTaskConfigFactory
    )

    def get_required_services(self):
        required_services = [DockerHostsService()]
        return required_services

    def get_services(self, project_configuration):
        return self.get_required_services() + list(project_configuration.get_secondary_services()) + [
            project_configuration.get_primary_service()]

    def factory_deployment_configs(self, project_configuration):
        services = self.get_services(project_configuration)
        factored_configs = []
        for service in services:
            factored_configs += service.factory_deployment_config()
        return factored_configs

    def deploy(self, project_configuration):
        configs = self.factory_default_configs() + self.factory_deployment_configs(project_configuration)
        return self._run_playbook(
            configs,
            hostname=project_configuration.hostname,
            password=None,
            username=project_configuration.username,
            port=project_configuration.port
        )