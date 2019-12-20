import React, {Component} from 'react';
import Flask from '../util/Flask';

class ArtistPage extends Component {
    
    constructor(props) {
        super(props)

        this.state = {
            artist: null
        }

    }

    componentDidMount() {
       this.loadArtistInfo();
    }

    loadArtistInfo() {
        let {mbid} = this.props.match.params
        Flask.getArtistById(mbid).then(artist => {
            this.setState({
                artist: artist
            })
        })
        
    }


    render() {

        const artist = this.state.artist;

        if (artist != null) {
            let count = 0;
            const predictions = artist.predictions.map(prediction => {
                    count++;
                    return (<p key={count}>{prediction}</p>)
                })
            
            return (
                <div>
                    <div className="ArtistPage-Wrapper">
            <h1 className="ArtistPageTitle">{artist.name} | {artist.country}</h1>
                        <h4 >Top {artist.predictions.length} Collaboration Predictions</h4>
                        {predictions}
                    </div>
                </div>
            )
        } else {
            return <div></div>
        }
    }
}
        
        



export default ArtistPage;