"""
Creates data visualizations for hierarchical Fides resource types.
"""

from typing import Generator, List, Dict

import plotly
import plotly.express as px
import plotly.graph_objects as go

from fidesctl.core import config

FIDES_KEY_NAME = "fides_key"
FIDES_PARENT_NAME = "parent_key"


def hierarchy_figures(
    categories: List[dict],
    resource_type: str,
    json_out: bool = False,
    condensed_html: bool = False,
) -> str:
    """
    Generate html to display a hierarchy with several representation options
    Args:
        categories: list of the dictionaries for each taxonomy member
        resource_type: the name of the resource type
        json_out: Flag to return a json representation of the visualization
        condensed_html: Flag to condense the result html but not including js and instead pointing to cdn
    Returns:
        Json representation of the figure if `json_out` is True, html otherwise
    """
    source = []
    target = []
    labels = []
    parents = []
    fides_key_dict = {}

    # build assets/relationships for figures
    for i, category in enumerate(categories):
        # get sunburst labels and parents
        labels.append(category[FIDES_KEY_NAME])
        parents.append(category[FIDES_PARENT_NAME])
        # build sankey mapping
        fides_key_dict[category[FIDES_KEY_NAME]] = i
        # assign colors for grouping in sunburst chart
        category["color"] = category[FIDES_KEY_NAME].split(".")[0]
        # get source and target paths for sankey and icicle graphs
        if FIDES_PARENT_NAME in category and category[FIDES_PARENT_NAME]:
            source.append(fides_key_dict[category[FIDES_PARENT_NAME]])
            target.append(fides_key_dict[category[FIDES_KEY_NAME]])

    fig_data = [
        go.Sunburst(labels=labels, parents=parents, hoverinfo="skip"),
        go.Sankey(
            valueformat=".1f",
            valuesuffix="%",
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=list(fides_key_dict.keys()),
                color="blue",  # Maybe make this 'ethyca blue'?
                # hovertemplate="%{label}",
            ),
            link=dict(source=source, target=target, value=target),
            visible=False,
            hoverinfo="skip",
        ),
        go.Icicle(labels=labels, parents=parents, visible=False, hoverinfo="skip"),
    ]

    fig = dict(
        data=fig_data,
        layout=dict(
            title=f'Fides {resource_type.replace("_", " ").title()} Hierarchy',
            showlegend=False,
            updatemenus=list(
                [
                    dict(
                        active=0,
                        buttons=list(
                            [
                                dict(
                                    label="Sunburst",
                                    method="update",
                                    args=[{"visible": [True, False, False]}],
                                ),
                                dict(
                                    label="Sankey",
                                    method="update",
                                    args=[{"visible": [False, True, False]}],
                                ),
                                dict(
                                    label="Icicle",
                                    method="update",
                                    args=[{"visible": [False, False, True]}],
                                ),
                            ]
                        ),
                    )
                ]
            ),
        ),
    )
    if json_out:
        return plotly.io.to_json(fig)
    return plotly.io.to_html(
        fig, include_plotlyjs="cdn" if condensed_html else True, full_html=True
    )


def sunburst_plot(
    categories: List[dict], resource_type: str, json_out: bool = False
) -> str:
    """
    Create a sunburst plot from data categories yaml file
    Reference: https://plotly.com/python/sunburst-charts/
    Args:
        categories: list of the dictionaries for each taxonomy member
        resource_type: the name of the resource type
        json_out: Flag to return a json representation of the visualization

    Returns:
        Json representation of the figure if `json_out` is True, html otherwise
    """

    # add color map
    for category in categories:
        category["color"] = category[FIDES_KEY_NAME].split(".")[0]

    fig = px.sunburst(
        categories, names=FIDES_KEY_NAME, parents=FIDES_PARENT_NAME, color="color"
    )
    fig.update_layout(
        title_text=f'Fides {resource_type.replace("_", " ").title()} Hierarchy',
        font_size=10,
    )

    if json_out:
        return fig.to_json()
    return fig.to_html()


def sankey_plot(
    categories: List[dict], resource_type: str, json_out: bool = False
) -> str:
    """
    Create a sankey plot from data categories yaml file
    Reference: https://plotly.com/python/sankey-diagram/
    Args:
        categories: list of the dictionaries for each taxonomy member
        resource_type: the name of the resource type
        json_out: Flag to return a json representation of the visualization

    Returns:
        Json representation of the figure if `json_out` is True, html otherwise
    """

    fides_key_dict = {v[FIDES_KEY_NAME]: i for i, v in enumerate(categories)}
    source = []
    target = []

    for category in categories:
        if FIDES_PARENT_NAME in category.keys():
            if category[FIDES_PARENT_NAME]:
                source.append(fides_key_dict[category[FIDES_PARENT_NAME]])
                target.append(fides_key_dict[category[FIDES_KEY_NAME]])

    fig = go.Figure(
        data=[
            go.Sankey(
                valueformat=".1f",
                valuesuffix="%",
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=list(fides_key_dict.keys()),
                    color="blue",  # Maybe make this 'ethyca blue'?
                    hovertemplate="%{label}",
                ),
                link=dict(source=source, target=target, value=target),
            )
        ]
    )

    fig.update_layout(
        title_text=f'Fides {resource_type.replace("_", " ").title()} Hierarchy',
        font_size=10,
    )

    if json_out:
        return fig.to_json()
    return fig.to_html()


def convert_categories_to_nested_dict(categories: List[dict]) -> dict:
    """
    Convert a catalog yaml file into a hierarchical nested dictionary.
    Leaf nodes will have an empty dictionary as the value.

    e.g.:

    {Parent1:
        {
            Child1: {},
            Child2: {},
            Parent2: {
                Child3: {}
                }
        }
    }

    Args:
        categories : list of dictionaries containing each entry from a catalog yaml file

    Returns:

    """

    def create_hierarchical_dict(data: dict, keys: List) -> None:
        """
        Create a nested dictionary given a list of strings as a key path
        Args:
            data: Dictionary to contain the nested dictionary as it's built
            keys: List of keys that equates to the 'path' down the nested dictionary

        Returns:
            None
        """
        for key in keys:
            if key in data:
                if key == keys[-1]:
                    # we've reached the end of the path (no more children)
                    data[key] = {}
                data = data[key]
            else:
                data[key] = {}

    nested_output: Dict[Dict, Dict] = {}
    for category in categories:
        if FIDES_PARENT_NAME not in category:
            nested_output[category[FIDES_KEY_NAME]] = {}
        else:
            node_path = category[FIDES_KEY_NAME].split(".")
            create_hierarchical_dict(nested_output, node_path)
    return nested_output


def nested_categories_to_html_list(
    categories: List[dict], resource_type: str, indent: int = 1
) -> str:
    """
    Create an HTML string unordered list from the keys of a nested dictionary
    Args:
        categories: list of the dictionaries for each taxonomy member
        resource_type: the name of the resource type
        indent: spacing multiplier

    Returns:

    """
    nested_categories = convert_categories_to_nested_dict(categories)

    def nest_to_html(nested_dict: dict, indent_factor: int) -> Generator:
        """
        Create the html
        Args:
            nested_dict: nested dictionary for keys to convert to html list object
            indent_factor: spacing multiplier

        Returns:
            HTML string containing a nested, unordered list of the nested dictionary keys
        """
        spacing = "   " * indent_factor
        for key, value in nested_dict.items():
            yield "{}<li>{}</li>".format(spacing, key)
            if isinstance(value, dict):
                yield "{spacing}<ul>\n{member}\n{spacing}</ul>".format(
                    spacing=spacing,
                    member="\n".join(nest_to_html(value, indent_factor + 1)),
                )

    header = f'<h2>Fides {resource_type.replace("_", " ").title()} Hierarchy</h2>'
    categories_tree = "\n".join(nest_to_html(nested_categories, indent))
    return f"{header}\n{categories_tree}"


def get_visualize_url(resource_type: str, visualize_type: str) -> str:
    """
    Get the url to the resource visualization web page
    Args:
        resource_type: Type of data fides resource ["data_category", "data_qualifier", "data_use"]
        visualize_type: type of UI to get a link to ["sankey", "sunburst", "text"]

    Returns:
        url string to the visualization
    """
    settings = config.get_config()
    visualize_url = "{}/{}/visualize/{}".format(
        settings.cli.server_url, resource_type, visualize_type
    )
    return visualize_url
