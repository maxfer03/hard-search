# Hard - search
Simple Flask + Vue webapp that searches on a dedicated list of good Hardware stores on Buenos Aires.

Something similar and in a bigger scale already exists called [HardGamers](https://www.hardgamers.com.ar/about/information), but most of the stores there are quite far away from where I leave or haven't updated their prices.

I needed a custom solution that would help me get quick prices on stores that I personally know and from whom I feel confident buying from, and this is it!



# To Run:

## Api
From `./api` folder:
Active a virtual environment and run:
```
pip install -r requirements.txt
flask run --debug
```

## Web Client
From `./client` folder:

```
npm i
npm run dev
```

Create a `.env.local` file and populate it with the required env variables
```
VITE_API_URL=your_api_url
```


# Usage
Use the `/search?query=` path to search by query.