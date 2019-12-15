import React, { Component } from 'react';

class SearchBar extends Component {
    constructor(props){
        super(props);
        this.state = {
            term: '',
            location: '', 
            sortBy: 'best_match'
        };

        this.handleTermChange = this.handleTermChange.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
    }

    handleTermChange(event) {
        this.setState({
            term: event.target.value
        });
    }

    handleSearch(event) {
        const term = this.state.term;
        this.props.searchArtist(term);
        event.preventDefault();
    }


    render() {
        return (
            <div className="SearchBar">

                <div className="SearchBar-fields">
                    <input placeholder="Search Artist" onChange={this.handleTermChange} />
                </div>
                <div className="SearchBar-submit">
                    <a onClick={this.handleSearch} >Let's Go</a>
                </div>
            </div>
        );
    }
}

export default SearchBar;