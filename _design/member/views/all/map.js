function(doc) {
  if (doc.doc_type == "Member") {
    emit(doc._id, doc);
  }
}
