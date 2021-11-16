import React from 'react';
import {UnControlled as CodeMirror} from 'react-codemirror2';
import './Editor.css';
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/blackboard.css';
require('codemirror/mode/python/python');

const state = {
    code: '',       // The code is stored here!!
    inputs: '',     // The inputs are stored here!!
    endpoint:"ws://localhost:8765",
    messages:'',
};

const handleInputChange = (event) => {
    state.inputs = event.target.value;
}

const componentDidMount = () => {
    const ws = new WebSocket(state.endpoint);
    ws.onopen = () => {
        console.log("Connected to Websocket 8765");
        ws.send(JSON.stringify({message:state.code, inputs:state.inputs}));
    }
    ws.onmessage = (evt) => {
        console.log(evt.data);
        state.messages = evt.data;
        document.getElementById("loadarea").innerHTML = 'Run';
        document.getElementById("output").value = state.messages;
        document.getElementById("submit").disabled = false;
    }
}

const handleSubmit = (event) => {
    document.getElementById("output").value = "";
    document.getElementById("submit").disabled = true;
    document.getElementById("loadarea").innerHTML = 'Loading <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span></div>';
    event.preventDefault();
    componentDidMount();
}

export default function CodeEditor() {
    return (
        <div>
            <center><h1>Python Interpreter</h1></center>
                <form onSubmit={handleSubmit}>
                    <div id="editor">
                        <CodeMirror
                            value='# Write your python code here...
print("hi")'
                            options={{
                                mode: 'python',
                                lineNumbers: true,
                                smartIndent: true,
                                theme: 'blackboard'
                            }}
                            onChange={(editor, data, value) => {
                                state.code = value
                            }}
                            defaultValue={null}
                        />
                    </div><br />

                    <center>
                        <button 
                            type = "submit" 
                            className="btn btn-primary btn-lg" 
                            onClick = {(event)=>handleSubmit(event)}
                            id = "submit"
                        >   
                            <div id = "loadarea">
                                &nbsp; Run &nbsp;
                            </div>
                        </button>
                        <div className="textAreaColumn">
                            <div>
                                <span><h2>Input</h2></span>
                                <textarea 
                                    id = "inputs" 
                                    cols="150" 
                                    rows="10" 
                                    defaultValue="" 
                                    onChange={(event) => handleInputChange(event)}
                                ></textarea>
                            </div>
                        <div>
                            <span><h2>Output</h2></span>
                            <textarea 
                                readOnly 
                                cols="150" 
                                rows="10" 
                                id="output"
                                value={state.messages}
                            ></textarea>
                        </div>
                    </div>
                </center>
            </form>    
        </div>
    )
}
