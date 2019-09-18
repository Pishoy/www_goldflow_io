from Jumpscale import j


class Package(j.baseclasses.threebot_package):
    def _init(self, **kwargs):
        if "branch" in kwargs.keys():
            self.branch = kwargs["branch"]
        else:
            self.branch = "master"

        self.goldflow_io_repo = "https://github.com/pishoy/www_goldflow_io"

    def prepare(self):
        """
        called when the 3bot starts
        :return:
        """

        server = j.servers.openresty.get("websites")
        server.install(reset=False)
        server.configure()
        website = server.websites.get("goldflow_io")
        website.ssl = False
        website.port = 80
        locations = website.locations.get("goldflow_io")

        website_location = locations.locations_static.new()
        website_location.name = "goldflow_io"
        website_location.path_url = "/"
        website_location.use_jumpscale_weblibs = True

        path = j.clients.git.getContentPathFromURLorPath(self.goldflow_io_repo, branch=self.branch, pull=True)
        j.sal.fs.chown(path, "www", "www")
        print (" this is the path {} ..............".format(path))
        website_location.path_location = path
        locations.configure()
        website.configure()

    def start(self):
        """
        called when the 3bot starts
        :return:
        """
        server = j.servers.openresty.get("websites")
        server.start()

    def stop(self):
        """
        called when the 3bot stops
        :return:
        """
        pass

    def uninstall(self):
        """
        called when the package is no longer needed and will be removed from the threebot
        :return:
        """
        pass
