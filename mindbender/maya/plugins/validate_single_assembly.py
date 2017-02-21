import pyblish.api


class ValidateMindbenderSingleAssembly(pyblish.api.InstancePlugin):
    """Each asset must have a single top-level group

    The given instance is test-exported, along with construction
    history to test whether more than 1 top-level DAG node would
    be included in the exported file.

    """

    label = "Validate Single Assembly"
    order = pyblish.api.ValidatorOrder
    hosts = ["maya"]
    families = ["mindbender.model", "mindbender.rig"]

    def process(self, instance):
        from maya import cmds
        from mindbender import maya

        with maya.maintained_selection():
            cmds.select(instance, replace=True)
            nodes = cmds.file(
                constructionHistory=True,
                exportSelected=True,
                preview=True,
                force=True,
            )

        assemblies = cmds.ls(nodes, assemblies=True)

        if not assemblies:
            raise Exception("No assembly found.")

        if len(assemblies) != 1:
            assemblies = '"%s"' % '", "'.join(assemblies)
            raise Exception(
                "Multiple assemblies found: %s" % assemblies
            )