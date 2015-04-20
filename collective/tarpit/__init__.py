import install
import patches


install.register_tarpit_plugin()
patches.patch_z_log()


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    install.register_tarpit_plugin_class(context)
