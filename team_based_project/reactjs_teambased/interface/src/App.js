import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

class App extends Component {

  
 
      state = {
        selectedFile: null,
      }
     

  
  onChangeHandler=event=>{

    this.setState({
      selectedFile: event.target.files[0]
    }, () => {
      console.log("state", this.state.selectedFile.name)
    })
    
    // console.log(this.state.selectedFile.name)
  } 

  onClickHandler = () => {
    const data = new FormData() 
    data.append('file', this.state.selectedFile)
    axios.post("http://localhost:5000/", data, { // receive two parameter endpoint url ,form data 
  })
  .then(res => { // then print response status
    console.log(res.statusText)
  })
  }

  
  downloadClickHandler = () => {
    //const urlDowload = "http://localhost:5000/downloads/Screenshot_from_2019-12-09_22-37-37.png"
    const urlDowload = "http://localhost:5000/downloads/out_" + this.state.selectedFile.name
    console.log(urlDowload)
    axios({
      url: urlDowload,
      method: 'GET',
      responseType: 'blob', // important
    }).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'file.docx');
      document.body.appendChild(link);
      link.click();
    });

  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>DEMONSTRATION</h2>
        </div>

        <div className="row">
          <h2>Team A</h2>
          <h3>Students: Anh Van Vu and Soyeon</h3>
          <h3>Course: Service Oriented Computing</h3>
        </div>

        <div className="row">
          <hr />
          <h3>Upload Document To Add Captions</h3>
          <input type="file" name="file" onChange={this.onChangeHandler}/>
          <button type="button" className="btn btn-success btn-block" onClick={this.onClickHandler}>Upload</button>
          <button type="button" className="btn btn-success btn-block" onClick={this.downloadClickHandler}>Download</button>
        </div>
      </div>
    );
  }
}

export default App;
