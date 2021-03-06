import os
import platform

import ftrack_template


def dictionary_to_paths(data, path="", results=[]):

    for key, value in data.iteritems():

        parent_path = (path + os.sep + key)
        if not path:
            parent_path = key

        if isinstance(value, dict):
            if "isfile" in value:
                temp = ftrack_template.Template("template", parent_path)
                temp.isfile = value["isfile"]
                temp.source = value["source"]
                results.append(temp)
            else:
                temp = ftrack_template.Template("template", parent_path)
                temp.isfile = False
                results.append(temp)
                if value:
                    dictionary_to_paths(
                        value, path=parent_path, results=results
                    )

    return results


def register():
    '''Register templates.'''

    system_name = platform.system().lower()
    if system_name != "windows":
        system_name = "unix"

    mount = (
        "{#project.disk." + system_name + "}/{#project.root}"
    )
    task = "{#task.name}"
    tasks = "tasks/" + task
    assetversion = "{#assetversion.asset.type.short}/v{#assetversion.version}"
    file_component = "{#component.name}{#component.file_type}"
    sequence_component = (
        "{#container.name}/{#container.name}.{#component.name}" +
        "{#component.file_type}"
    )
    assets = "library/{#assetbuild.type.name}/{#assetbuild.name}"
    shot = "{#shot.name}"
    shots = "shots/" + shot
    sequence = "{#sequence.name}"
    sequences = "sequences/" + sequence
    episode = "{#episode.name}"
    episodes = "episodes/" + episode

    task_structure = {
        "work": {
            "{maya}": {
                "maya_v{padded_version}.mb": {
                    "isfile": True,
                    "source": os.path.join(
                        os.path.dirname(__file__), "maya.mb"
                    )
                }
            },
            "{hiero}": {
                "hiero_v{padded_version}.hrox": {
                    "isfile": True,
                    "source": os.path.join(
                        os.path.dirname(__file__), "hiero.hrox"
                    )
                }
            },
            "{nuke}": {
                "nuke_v{padded_version}.nk": {
                    "isfile": True,
                    "source": os.path.join(
                        os.path.dirname(__file__), "nuke.nk"
                    )
                }
            }
        },
        "publish": {
            assetversion: {
                file_component: {},
                sequence_component: {}
            }
        }
    }

    project_structure = {
        mount: {
            tasks: task_structure,
            assets: {
                task: task_structure
            },
            shots: {
                task: task_structure,
                assets: {
                    task: task_structure
                },
            },
            sequences: {
                task: task_structure,
                assets: {
                    task: task_structure
                },
                shot: {
                    task: task_structure,
                    assets: {
                        task: task_structure
                    }
                }
            },
            episodes: {
                task: task_structure,
                assets: {
                    task: task_structure
                },
                shot: {
                    task: task_structure,
                    assets: {
                        task: task_structure
                    }
                },
                sequence: {
                    task: task_structure,
                    assets: {
                        task: task_structure
                    },
                    shot: {
                        task: task_structure,
                        assets: {
                            task: task_structure
                        }
                    }
                },
            }
        }
    }

    return dictionary_to_paths(project_structure)
