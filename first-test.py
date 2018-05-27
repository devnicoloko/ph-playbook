"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'list_channels_1' block
    list_channels_1(container=container)

    # call 'format_1' block
    format_1(container=container)

    return

def send_message_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('send_message_2() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'send_message_2' call
    filtered_results_data_1 = phantom.collect2(container=container, datapath=["filtered-data:filter_1:condition_1:list_channels_1:action_result.data.*.channels.*.name", "filtered-data:filter_1:condition_1:list_channels_1:action_result.parameter.context.artifact_id"])
    formatted_data_1 = phantom.get_format_data(name='format_1')

    parameters = []
    
    # build parameters list for 'send_message_2' call
    for filtered_results_item_1 in filtered_results_data_1:
        if filtered_results_item_1[0]:
            parameters.append({
                'destination': filtered_results_item_1[0],
                'message': formatted_data_1,
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_results_item_1[1]},
            })

    phantom.act("send message", parameters=parameters, assets=['slack'], name="send_message_2", parent_action=action)

    return

def join_send_message_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_send_message_2() called')

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'list_channels_1' ]):
        
        # call connected block "send_message_2"
        send_message_2(container=container, handle=handle)
    
    return

def list_channels_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('list_channels_1() called')

    parameters = []

    phantom.act("list channels", parameters=parameters, assets=['slack'], callback=filter_1, name="list_channels_1")

    return

def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('filter_1() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["list_channels_1:action_result.data.*.channels.*.name", "==", "#demo"],
        ],
        name="filter_1:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        join_send_message_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('format_1() called')
    
    template = """{0} |{1}"""

    # parameter list for template variable replacement
    parameters = [
        "container:description",
        "container:severity",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    join_send_message_2(container=container)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return