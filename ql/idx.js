const { Neo4jGraphQL } = require("@neo4j/graphql");
const neo4j = require("neo4j-driver");
const { ApolloServer } = require("apollo-server");

const typeDefs = `
    type Movie {
        title: String
        year: Int
        imdbRating: Float
        genres: [Genre!]! @relationship(type: "IN_GENRE", direction: OUT)
    }

    type Genre {
        name: String
        movies: [Movie!]! @relationship(type: "IN_GENRE", direction: IN)
    }
`;

const driver = neo4j.driver("bolt://localhost:7687", neo4j.auth.basic("neo4j", "letmein"));

const neoSchema = new Neo4jGraphQL({ typeDefs, driver });

async function main() {
    const schema = await neoSchema.getSchema();

    const server = new ApolloServer({
        schema,
        context: ({ req }) => ({ req }),
    });

    await server.listen(4000);

    console.log("Online");
}