import React, { Component } from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import Header from './Components/Header';
import ArtistList from './Components/ArtistList';
import ArtistPage from './Components/ArtistPage';
import './App.css';
import Flask from './util/Flask';

import Test from './Components/Test';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      artists: [],
      searchResults: [],
      selectedArtist: null
    }

    this.selectArtist = this.selectArtist.bind(this)

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

  selectArtist(artistId) {
    Flask.getArtistById(artistId)
    .then(artist => {
      this.setState({
        selectedArtist: artist
      })
    })
  }

  render() {

    //<Route path="/artists/:mbid" component={() => <ArtistPage selectArtist={this.selectArtist} /> } />

    return ( 
      <BrowserRouter>
        <div className="App">
          <Header />
          <Switch>
            <Route path="/artists/:mbid" component={ArtistPage} />
            <Route exact path="/" component={() => <ArtistList artists={this.state.artists} selectArtist={this.selectArtist} />} />
            <Redirect to="/" />
          </Switch>
        </div>
      </BrowserRouter>
    )
      
  }
}


export default App;
