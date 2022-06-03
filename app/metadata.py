# obsolete:  TODO: delete

import datalayer
from datalayer.provider_node import ProviderNodeCallbacks, NodeCallback
from datalayer.variant import Result, Variant

import flatbuffers
from comm.datalayer import Metadata, NodeClass, AllowedOperations, Reference


def create(self, typeAddress: str, name: str, description: str):

    # Create `FlatBufferBuilder`instance. Initial Size 1024 bytes (grows automatically if needed)
    builder = flatbuffers.Builder(1024)

    # Serialize AllowedOperations data
    AllowedOperations.AllowedOperationsStart(builder)
    AllowedOperations.AllowedOperationsAddRead(builder, True)
    AllowedOperations.AllowedOperationsAddWrite(builder, True)
    AllowedOperations.AllowedOperationsAddCreate(builder, False)
    AllowedOperations.AllowedOperationsAddDelete(builder, False)
    operations = AllowedOperations.AllowedOperationsEnd(builder)

    # Metadata description strings
    descriptionBuilderString = builder.CreateString(description)
    #urlBuilderString = builder.CreateString("tbd")
    displayNameString = builder.CreateString(name)
    #unitString = builder.CreateString(unit)

    # Store string parameter into builder
    readTypeBuilderString = builder.CreateString("readType")
    writeTypeBuilderString = builder.CreateString("writeType")
    #createTypeBuilderString = builder.CreateString("createType")
    targetAddressBuilderString = builder.CreateString(typeAddress)

    # Serialize Reference data (for read operation)
    Reference.ReferenceStart(builder)
    Reference.ReferenceAddType(builder, readTypeBuilderString)
    Reference.ReferenceAddTargetAddress(
        builder, targetAddressBuilderString)
    reference_read = Reference.ReferenceEnd(builder)

    # Serialize Reference data (for write operation)
    Reference.ReferenceStart(builder)
    Reference.ReferenceAddType(builder, writeTypeBuilderString)
    Reference.ReferenceAddTargetAddress(
        builder, targetAddressBuilderString)
    reference_write = Reference.ReferenceEnd(builder)

    # Create FlatBuffer vector and prepend reference data. Note: Since we prepend the data, prepend them in reverse order.
    Metadata.MetadataStartReferencesVector(builder, 2)
    # builder.PrependSOffsetTRelative(reference_create)
    builder.PrependSOffsetTRelative(reference_write)
    builder.PrependSOffsetTRelative(reference_read)
    references = builder.EndVector(2)

    # Serialize Metadata data
    Metadata.MetadataStart(builder)
    Metadata.MetadataAddNodeClass(builder, NodeClass.NodeClass.Variable)
    Metadata.MetadataAddOperations(builder, operations)
    Metadata.MetadataAddDescription(builder, descriptionBuilderString)
    #Metadata.MetadataAddDescriptionUrl(builder, urlBuilderString)
    Metadata.MetadataAddDisplayName(builder, displayNameString)
    #Metadata.MetadataAddUnit(builder, unitString)

    # Metadata reference table
    Metadata.MetadataAddReferences(builder, references)
    metadata = Metadata.MetadataEnd(builder)

    # Closing operation
    builder.Finish(metadata)
    result = self.metadata.set_flatbuffers(builder.Output())
    if result != datalayer.variant.Result.OK:
        print("ERROR creating metadata failed with: ", result)