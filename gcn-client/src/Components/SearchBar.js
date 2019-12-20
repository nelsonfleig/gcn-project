import React, { Component } from 'react';

class SearchBar extends Component {
    constructor(props){
        super(props);
        this.state = {
            term: ''
        };

        this.handleTermChange = this.handleTermChange.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
        this.handleClear = this.handleClear.bind(this);
    }

    handleTermChange(event) {
        this.setState({
            term: event.target.value
        });
    }

    handleSearch(event) {
        
        const term = this.state.term;
        this.props.searchArtists(term);
        event.preventDefault();
    }

    handleClear() {
        this.props.clearSearch()
    }

    render() {

        console.log(this.state.term)
        return (
            <div className="SearchBar">

                <div className="SearchBar-fields">
                    <input placeholder="Search artist" onChange={this.handleTermChange} onKeyDown={event => {
                        if (event.key === 'Enter') {
                        this.handleSearch(event)
                        }
                    }} />
                </div>
                <div className="SearchBar-submit">
                    <button onClick={this.handleSearch} >Search</button>
                    <button onClick={this.handleClear} >Clear</button>
                </div>
            </div>
        );
    }
}

export default SearchBar;