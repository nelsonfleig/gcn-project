import React, { Component } from 'react';
import { Navbar, NavbarBrand } from 'reactstrap';
import ArtistList from './Components/ArtistList/ArtistList';
import './App.css';
import Flask from './util/Flask';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      artists: []
    }
  }

  componentDidMount(){
    this.loadArtists()
  }

  loadArtists() {
    Flask.getArtists().then( artists => {
      this.setState({
        artists: artists
      });
    });
  }

  render() {
    return (
      <div className="App">
        <Navbar dark color="primary">
          <div className="container">
            <NavbarBrand href="/">GCN App</NavbarBrand>
          </div>
        </Navbar>
        <ArtistList artists={this.state.artists}></ArtistList>
      </div>
    );
  }
}

export default App;
