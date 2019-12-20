import React, { Component } from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import Header from './Components/Header';
import ArtistList from './Components/ArtistList';
import ArtistPage from './Components/ArtistPage';
import './App.css';
import Flask from './util/Flask';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      artists: [],
      searchResults: [],
      selectedArtist: null
    }

    this.selectArtist = this.selectArtist.bind(this)
    this.searchArtists = this.searchArtists.bind(this)
    this.clearSearch = this.clearSearch.bind(this)
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

  searchArtists(term) {
    Flask.search(term).then( artists => {
      this.setState({
        searchResults: artists
      })
    })
  }

  clearSearch() {
    this.setState({
      searchResults: []
    })
  }

  render() {

    return ( 
      <BrowserRouter>
        <div className="App">
          <Header />
          <Switch>
            <Route path="/artists/:mbid" component={ArtistPage} />
            <Route exact path="/" component={() => <ArtistList artists={this.state.artists} selectArtist={this.selectArtist} searchArtists={this.searchArtists} searchResults={this.state.searchResults} clearSearch={this.clearSearch} />} />
            <Redirect to="/" />
          </Switch>
        </div>
      </BrowserRouter>
    )
      
  }
}


export default App;
