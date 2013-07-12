function(doc) {
  if (doc.doc_type == "AccessMethod") {
    emit(doc._id, doc);
  }
}
