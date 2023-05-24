from TicketChunker import TicketChunker
def uploadTicket(TicketID):
    chunks = TicketChunker.chunkTicket(TicketID)
    col = initMongo()
    index = initPinecone()

    for chunk in chunks:
        uploadChunk(chunk, index, col)
